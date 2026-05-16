# integrated_agent_system.py - Integration of all agents
from datetime import datetime
import threading
import time

class IntegratedAgentSystem:
    """Integrated system that coordinates all real agents"""
    
    def __init__(self, market_agent, technical_agent):
        self.market_agent = market_agent
        self.technical_agent = technical_agent
        self.pattern_agent = PatternRecognitionAgent()
        self.risk_agent = RiskAssessmentAgent()
        self.alert_agent = AlertGenerationAgent()
        
        self.running = False
        self.coordination_data = {
            "latest_market_data": [],
            "latest_signals": [],
            "latest_patterns": [],
            "latest_risk_metrics": {},
            "latest_alerts": []
        }
    
    def coordinate_agents(self):
        """Main coordination loop that runs all agents together"""
        print(f"🤖 Starting integrated agent coordination...")
        
        # Step 1: Collect market data
        print("📊 Market Data Agent: Collecting live data...")
        market_data = self.market_agent.collect_all_data()
        self.coordination_data["latest_market_data"] = market_data
        
        # Step 2: Generate technical signals
        print("🧠 Technical Analysis Agent: Analyzing trends...")
        signals = []
        for stock in market_data:
            signal = self.technical_agent.analyze_stock(stock["symbol"], stock["price"])
            signals.append(signal)
        self.coordination_data["latest_signals"] = signals
        
        # Step 3: Pattern recognition analysis
        print("🔍 Pattern Recognition Agent: Detecting patterns...")
        all_patterns = []
        for stock in market_data:
            patterns = self.pattern_agent.analyze_patterns(stock["symbol"], stock)
            all_patterns.extend(patterns)
        self.coordination_data["latest_patterns"] = all_patterns
        
        # Step 4: Risk assessment
        print("⚖️ Risk Assessment Agent: Calculating portfolio risk...")
        portfolio_data = {"total_value": 50000, "positions": market_data}
        risk_metrics = self.risk_agent.comprehensive_risk_analysis(portfolio_data, market_data)
        self.coordination_data["latest_risk_metrics"] = risk_metrics
        
        # Step 5: Generate alerts
        print("🚨 Alert Generation Agent: Creating intelligent alerts...")
        new_alerts = []
        
        # Generate trading signal alerts
        for signal in signals:
            if signal["signal"] in ["BUY", "SELL"]:
                # Find corresponding pattern if exists
                related_pattern = None
                for pattern in all_patterns:
                    if pattern["symbol"] == signal["symbol"]:
                        related_pattern = pattern
                        break
                
                alert = self.alert_agent.create_alert(
                    signal_data=signal,
                    pattern_data=related_pattern,
                    risk_data=risk_metrics.get("portfolio_risk")
                )
                if alert:
                    new_alerts.append(alert)
        
        # Generate pattern alerts
        for pattern in all_patterns:
            if pattern["probability"] > 0.75:  # High probability patterns
                pattern_alert = self.alert_agent.create_pattern_alert(pattern)
                if pattern_alert:
                    new_alerts.append(pattern_alert)
        
        # Generate risk alerts
        risk_alerts = self.alert_agent.create_risk_alert(risk_metrics)
        new_alerts.extend(risk_alerts)
        
        self.coordination_data["latest_alerts"] = new_alerts
        
        # Step 6: Summary
        print(f"✅ Agent coordination complete:")
        print(f"   📈 Market data points: {len(market_data)}")
        print(f"   🎯 Trading signals: {len(signals)}")
        print(f"   🔍 Patterns detected: {len(all_patterns)}")
        print(f"   ⚖️ Risk factors: {len(risk_metrics.get('risk_factors', []))}")
        print(f"   🚨 Alerts generated: {len(new_alerts)}")
        
        return self.coordination_data
    
    def start_continuous_coordination(self, interval_seconds=60):
        """Start continuous agent coordination"""
        self.running = True
        
        def coordination_loop():
            while self.running:
                try:
                    self.coordinate_agents()
                    time.sleep(interval_seconds)
                except Exception as e:
                    print(f"❌ Coordination error: {e}")
                    time.sleep(30)  # Wait 30 seconds before retry
        
        coordination_thread = threading.Thread(target=coordination_loop)
        coordination_thread.daemon = True
        coordination_thread.start()
        
        return coordination_thread
    
    def stop_coordination(self):
        """Stop the continuous coordination"""
        self.running = False
        print("🛑 Agent coordination stopped")
    
    def get_agent_statistics(self):
        """Get comprehensive statistics from all agents"""
        return {
            "pattern_recognition": self.pattern_agent.get_accuracy_stats(),
            "alert_generation": self.alert_agent.get_alert_statistics(),
            "market_data": {
                "symbols_monitored": len(self.coordination_data["latest_market_data"]),
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "technical_analysis": {
                "signals_generated": len(self.coordination_data["latest_signals"]),
                "buy_signals": len([s for s in self.coordination_data["latest_signals"] if s.get("signal") == "BUY"]),
                "sell_signals": len([s for s in self.coordination_data["latest_signals"] if s.get("signal") == "SELL"])
            },
            "risk_assessment": {
                "portfolio_risk_score": self.coordination_data["latest_risk_metrics"].get("portfolio_risk", {}).get("overall_score", 0),
                "risk_factors_identified": len(self.coordination_data["latest_risk_metrics"].get("risk_factors", []))
            }
        }
