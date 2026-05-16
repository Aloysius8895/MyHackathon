# alert_generation_agent.py - REAL Alert Generation Agent
from datetime import datetime
import json

class AlertGenerationAgent:
    """Real Alert Generation Agent that generates intelligent, personalized notifications"""
    
    def __init__(self):
        self.name = "Alert Generation Agent"
        self.alert_history = []
        self.user_preferences = {
            "risk_tolerance": "medium",
            "alert_threshold": 0.7,
            "preferred_signals": ["BUY", "SELL"],
            "max_alerts_per_hour": 5,
            "notification_channels": ["dashboard", "email"]
        }
        self.alert_counter = 0
        
    def set_user_preferences(self, preferences):
        """Update user alert preferences"""
        self.user_preferences.update(preferences)
    
    def should_generate_alert(self, signal_data):
        """Determine if an alert should be generated based on signal quality and user preferences"""
        # Check if signal type is in user preferences
        if signal_data.get("signal") not in self.user_preferences["preferred_signals"]:
            return False
        
        # Check signal confidence against user threshold
        confidence = self._calculate_signal_confidence(signal_data)
        if confidence < self.user_preferences["alert_threshold"]:
            return False
        
        # Check rate limiting
        recent_alerts = self._get_recent_alerts(hours=1)
        if len(recent_alerts) >= self.user_preferences["max_alerts_per_hour"]:
            return False
        
        # Check for duplicate alerts
        if self._is_duplicate_alert(signal_data):
            return False
        
        return True
    
    def _calculate_signal_confidence(self, signal_data):
        """Calculate confidence score for a signal"""
        base_confidence = 0.5
        
        # Boost confidence for strong signals
        if signal_data.get("signal") in ["BUY", "SELL"]:
            base_confidence += 0.2
        
        # Boost confidence if multiple indicators align
        reason = signal_data.get("reason", "").lower()
        if "rsi" in reason and "macd" in reason:
            base_confidence += 0.2
        
        # Boost confidence for oversold/overbought conditions
        if "oversold" in reason or "overbought" in reason:
            base_confidence += 0.15
        
        # Boost confidence for strong price movements
        if "breakout" in reason or "breakdown" in reason:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _get_recent_alerts(self, hours=1):
        """Get alerts from the last N hours"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        return [alert for alert in self.alert_history 
                if alert.get("timestamp_unix", 0) > cutoff_time]
    
    def _is_duplicate_alert(self, signal_data):
        """Check if this alert is a duplicate of recent alerts"""
        recent_alerts = self._get_recent_alerts(hours=2)
        
        for alert in recent_alerts:
            if (alert.get("symbol") == signal_data.get("symbol") and 
                alert.get("type") == signal_data.get("signal")):
                return True
        return False
    
    def generate_personalized_message(self, signal_data):
        """Generate personalized alert message based on user preferences and signal data"""
        symbol = signal_data.get("symbol", "Unknown")
        signal_type = signal_data.get("signal", "HOLD")
        price = signal_data.get("price", 0)
        reason = signal_data.get("reason", "Technical analysis")
        
        # Base message templates
        templates = {
            "BUY": [
                f"🚀 Strong BUY signal for {symbol} at ${price}",
                f"📈 {symbol} showing bullish momentum at ${price}",
                f"💡 Technical analysis suggests buying {symbol} at ${price}"
            ],
            "SELL": [
                f"⚠️ SELL signal triggered for {symbol} at ${price}",
                f"📉 Consider selling {symbol} - current price ${price}",
                f"🔴 Technical indicators suggest selling {symbol}"
            ],
            "HOLD": [
                f"⏸️ Hold position in {symbol} - mixed signals at ${price}",
                f"🤔 {symbol} showing neutral momentum at ${price}"
            ]
        }
        
        # Select template based on user risk tolerance
        template_list = templates.get(signal_type, templates["HOLD"])
        
        if self.user_preferences["risk_tolerance"] == "aggressive":
            message = template_list[0]  # Most aggressive message
        elif self.user_preferences["risk_tolerance"] == "conservative":
            message = template_list[-1] if len(template_list) > 1 else template_list[0]  # Most conservative
        else:
            message = template_list[len(template_list)//2]  # Middle option
        
        # Add reasoning
        detailed_message = f"{message}\n💭 Reason: {reason}"
        
        return {
            "title": f"{signal_type} Signal: {symbol}",
            "message": message,
            "detailed_message": detailed_message,
            "urgency": self._calculate_urgency(signal_data)
        }
    
    def _calculate_urgency(self, signal_data):
        """Calculate urgency level for the alert"""
        confidence = self._calculate_signal_confidence(signal_data)
        signal_type = signal_data.get("signal", "HOLD")
        
        if confidence > 0.8 and signal_type in ["BUY", "SELL"]:
            return "high"
        elif confidence > 0.6 and signal_type in ["BUY", "SELL"]:
            return "medium"
        else:
            return "low"
    
    def create_alert(self, signal_data, pattern_data=None, risk_data=None):
        """Create a comprehensive alert with multiple data sources"""
        if not self.should_generate_alert(signal_data):
            return None
        
        # Generate personalized message
        message_data = self.generate_personalized_message(signal_data)
        
        # Create comprehensive alert
        alert = {
            "id": f"alert_{self.alert_counter}_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp_unix": datetime.now().timestamp(),
            "type": signal_data.get("signal", "HOLD"),
            "symbol": signal_data.get("symbol", "Unknown"),
            "price": signal_data.get("price", 0),
            "confidence": self._calculate_signal_confidence(signal_data),
            "urgency": message_data["urgency"],
            "title": message_data["title"],
            "message": message_data["message"],
            "detailed_message": message_data["detailed_message"],
            "reason": signal_data.get("reason", "Technical analysis"),
            "agent": "alert_generation_agent",
            "channels": self.user_preferences["notification_channels"],
            "source_data": {
                "signal": signal_data,
                "pattern": pattern_data,
                "risk": risk_data
            }
        }
        
        # Add pattern information if available
        if pattern_data:
            alert["pattern_detected"] = pattern_data.get("pattern_name", "Unknown")
            alert["pattern_probability"] = pattern_data.get("probability", 0)
            alert["message"] += f" (Pattern: {pattern_data.get('pattern_name', 'Unknown')})"
        
        # Add risk information if available
        if risk_data:
            alert["risk_level"] = risk_data.get("risk_level", "Medium")
            alert["risk_score"] = risk_data.get("overall_score", 0.5)
        
        self.alert_counter += 1
        self.alert_history.append(alert)
        
        return alert
    
    def create_risk_alert(self, risk_data):
        """Create risk-specific alerts"""
        alerts = []
        
        # VaR breach alert
        portfolio_risk = risk_data.get("portfolio_risk", {})
        var_amount = portfolio_risk.get("var_1day", 0)
        
        if var_amount > 4000:
            alert = {
                "id": f"risk_alert_{self.alert_counter}_{int(datetime.now().timestamp())}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_unix": datetime.now().timestamp(),
                "type": "RISK",
                "title": "⚠️ High Portfolio Risk Detected",
                "message": f"Portfolio VaR exceeds ${var_amount:,.0f}",
                "urgency": "high",
                "category": "risk_management",
                "agent": "alert_generation_agent"
            }
            alerts.append(alert)
            self.alert_counter += 1
        
        # Correlation alert
        correlations = risk_data.get("correlation_matrix", {})
        high_correlations = [k for k, v in correlations.items() if abs(v) > 0.8]
        
        if high_correlations:
            alert = {
                "id": f"corr_alert_{self.alert_counter}_{int(datetime.now().timestamp())}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_unix": datetime.now().timestamp(),
                "type": "CORRELATION",
                "title": "🔗 High Asset Correlation Warning",
                "message": f"High correlation detected: {', '.join(high_correlations[:2])}",
                "urgency": "medium",
                "category": "risk_management",
                "agent": "alert_generation_agent"
            }
            alerts.append(alert)
            self.alert_counter += 1
        
        # Risk level alert
        risk_level = portfolio_risk.get("risk_level", "Medium")
        if risk_level == "High":
            alert = {
                "id": f"risk_level_alert_{self.alert_counter}_{int(datetime.now().timestamp())}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_unix": datetime.now().timestamp(),
                "type": "RISK_LEVEL",
                "title": "🚨 Portfolio Risk Level: HIGH",
                "message": f"Portfolio risk assessment indicates HIGH risk level",
                "urgency": "high",
                "category": "risk_management",
                "agent": "alert_generation_agent"
            }
            alerts.append(alert)
            self.alert_counter += 1
        
        self.alert_history.extend(alerts)
        return alerts
    
    def create_pattern_alert(self, pattern_data):
        """Create pattern-specific alerts"""
        probability = pattern_data.get("probability", 0)
        if probability < 0.7:
            return None
        
        symbol = pattern_data.get("symbol", "Unknown")
        pattern_name = pattern_data.get("pattern_name", "Pattern")
        
        alert = {
            "id": f"pattern_alert_{self.alert_counter}_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp_unix": datetime.now().timestamp(),
            "type": "PATTERN",
            "symbol": symbol,
            "title": f"🔍 {pattern_name} Detected",
            "message": f"{symbol} shows {pattern_name} with {probability*100:.0f}% probability",
            "urgency": "high" if probability > 0.8 else "medium",
            "category": "pattern_recognition",
            "pattern_details": pattern_data,
            "agent": "alert_generation_agent"
        }
        
        self.alert_counter += 1
        self.alert_history.append(alert)
        return alert
    
    def get_alert_statistics(self):
        """Get statistics about generated alerts"""
        total_alerts = len(self.alert_history)
        if total_alerts == 0:
            return {"total": 0, "by_type": {}, "by_urgency": {}}
        
        # Count by type
        by_type = {}
        by_urgency = {}
        
        for alert in self.alert_history:
            alert_type = alert.get("type", "Unknown")
            urgency = alert.get("urgency", "low")
            
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
            by_urgency[urgency] = by_urgency.get(urgency, 0) + 1
        
        return {
            "total": total_alerts,
            "by_type": by_type,
            "by_urgency": by_urgency,
            "recent_24h": len([a for a in self.alert_history 
                             if a.get("timestamp_unix", 0) > datetime.now().timestamp() - 86400])
        }