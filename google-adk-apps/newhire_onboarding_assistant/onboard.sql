-- Create database for onboard data
CREATE DATABASE onboard_data;

-- Connect to the new database
\c onboard_data;

-- Create main table for storing JSON documents
CREATE TABLE json_documents (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50),
    filename VARCHAR(255) NOT NULL,
    document_type VARCHAR(50),
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_json_documents_category ON json_documents(category);
CREATE INDEX idx_json_documents_subcategory ON json_documents(subcategory);
CREATE INDEX idx_json_documents_filename ON json_documents(filename);
CREATE INDEX idx_json_documents_type ON json_documents(document_type);

-- Create GIN index for JSON queries
CREATE INDEX idx_json_documents_data ON json_documents USING GIN (data);

-- Create function to update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for auto-updating timestamp
CREATE TRIGGER update_json_documents_updated_at 
    BEFORE UPDATE ON json_documents 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();




-- ============================================================================
-- COMPLETE INSERT SCRIPT FOR ALL JSON DATA
-- ============================================================================

-- 1. TEAMS DATA
-- ============================================================================

-- Team Members
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('teams', 'members', 'team_members.json', 'team_info', '{
  "members": [
    {
      "name": "Alice Chen",
      "role": "Senior Backend Engineer",
      "team": "Backend Authentication Team",
      "email": "alice.chen@company.com",
      "slack_handle": "@alice.chen",
      "expertise": ["Authentication", "Security", "Python", "JWT", "OAuth2"],
      "bio": "8 years of experience in backend development with focus on security and authentication systems. Previously worked at major tech companies on identity management.",
      "location": "San Francisco, CA",
      "timezone": "PST",
      "availability": "Generally available 9 AM - 6 PM PST",
      "fun_fact": "Amateur rock climber and coffee enthusiast"
    },
    {
      "name": "Bob Johnson",
      "role": "Backend Engineer",
      "team": "Backend Authentication Team",
      "email": "bob.johnson@company.com",
      "slack_handle": "@bob.j",
      "expertise": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
      "bio": "5 years in backend development. Passionate about building scalable microservices and clean APIs.",
      "location": "Seattle, WA",
      "timezone": "PST",
      "availability": "Available 8 AM - 5 PM PST",
      "fun_fact": "Plays guitar in a local band on weekends"
    },
    {
      "name": "Carol White",
      "role": "Backend Engineer",
      "team": "Backend Authentication Team",
      "email": "carol.white@company.com",
      "slack_handle": "@carol.white",
      "expertise": ["Session Management", "Redis", "Python", "Security", "Testing"],
      "bio": "4 years of experience with focus on session management and caching strategies. Strong advocate for comprehensive testing.",
      "location": "Austin, TX",
      "timezone": "CST",
      "availability": "Available 10 AM - 7 PM CST",
      "fun_fact": "Marathon runner and yoga instructor"
    },
    {
      "name": "Eric Wang",
      "role": "Senior Payment Engineer",
      "team": "Payments Team",
      "email": "eric.wang@company.com",
      "slack_handle": "@eric.wang",
      "expertise": ["Payment Systems", "Stripe", "PayPal", "PCI Compliance", "Django"],
      "bio": "10 years specializing in payment systems and financial integrations. Expert in PCI compliance and payment security.",
      "location": "New York, NY",
      "timezone": "EST",
      "availability": "Available 9 AM - 6 PM EST",
      "fun_fact": "Collects vintage keyboards and loves mechanical switches"
    },
    {
      "name": "Grace Kim",
      "role": "Fraud Detection Engineer",
      "team": "Payments Team",
      "email": "grace.kim@company.com",
      "slack_handle": "@grace.kim",
      "expertise": ["Machine Learning", "Fraud Detection", "Python", "TensorFlow", "Data Analysis"],
      "bio": "6 years in ML engineering with focus on fraud detection and anomaly detection systems.",
      "location": "Los Angeles, CA",
      "timezone": "PST",
      "availability": "Available 10 AM - 7 PM PST",
      "fun_fact": "Amateur astronomer with own telescope"
    },
    {
      "name": "Henry Taylor",
      "role": "Senior Frontend Engineer",
      "team": "Frontend Team",
      "email": "henry.taylor@company.com",
      "slack_handle": "@henry.t",
      "expertise": ["React", "TypeScript", "Performance Optimization", "Webpack", "CSS"],
      "bio": "9 years in frontend development. Passionate about web performance and user experience.",
      "location": "Portland, OR",
      "timezone": "PST",
      "availability": "Available 8 AM - 5 PM PST",
      "fun_fact": "Homebrewer and craft beer enthusiast"
    },
    {
      "name": "Isabel Martinez",
      "role": "Frontend Engineer",
      "team": "Frontend Team",
      "email": "isabel.martinez@company.com",
      "slack_handle": "@isabel.m",
      "expertise": ["React", "Accessibility", "CSS", "JavaScript", "Testing"],
      "bio": "5 years focused on accessible web development and inclusive design practices.",
      "location": "Chicago, IL",
      "timezone": "CST",
      "availability": "Available 9 AM - 6 PM CST",
      "fun_fact": "Volunteers teaching coding to underrepresented groups"
    },
    {
      "name": "Laura Anderson",
      "role": "Senior DevOps Engineer",
      "team": "Infrastructure Team",
      "email": "laura.anderson@company.com",
      "slack_handle": "@laura.a",
      "expertise": ["Kubernetes", "Terraform", "AWS", "CI/CD", "Monitoring"],
      "bio": "8 years in DevOps and infrastructure. Expert in cloud platforms and infrastructure automation.",
      "location": "Denver, CO",
      "timezone": "MST",
      "availability": "Available 8 AM - 5 PM MST",
      "fun_fact": "Avid hiker and has climbed 20 of Colorado''s fourteeners"
    },
    {
      "name": "Mark Thompson",
      "role": "Site Reliability Engineer",
      "team": "Infrastructure Team",
      "email": "mark.thompson@company.com",
      "slack_handle": "@mark.thompson",
      "expertise": ["SRE", "Monitoring", "Incident Response", "Python", "Go"],
      "bio": "7 years in SRE roles. Focused on system reliability, monitoring, and incident management.",
      "location": "Toronto, Canada",
      "timezone": "EST",
      "availability": "Available 9 AM - 6 PM EST, On-call rotation",
      "fun_fact": "Hockey player and coach for youth league"
    },
    {
      "name": "Olivia Parker",
      "role": "Senior Data Engineer",
      "team": "Data Engineering Team",
      "email": "olivia.parker@company.com",
      "slack_handle": "@olivia.p",
      "expertise": ["Apache Beam", "BigQuery", "Python", "Airflow", "Data Pipelines"],
      "bio": "9 years building data infrastructure and pipelines. Expert in batch and streaming data processing.",
      "location": "Boston, MA",
      "timezone": "EST",
      "availability": "Available 9 AM - 6 PM EST",
      "fun_fact": "Competitive chess player and puzzle enthusiast"
    },
    {
      "name": "Peter Zhang",
      "role": "ML Engineer",
      "team": "Data Engineering Team",
      "email": "peter.zhang@company.com",
      "slack_handle": "@peter.zhang",
      "expertise": ["Machine Learning", "TensorFlow", "PyTorch", "MLOps", "Python"],
      "bio": "6 years in ML engineering. Specializes in productionizing ML models and building ML platforms.",
      "location": "San Diego, CA",
      "timezone": "PST",
      "availability": "Available 10 AM - 7 PM PST",
      "fun_fact": "Amateur photographer specializing in landscape photography"
    },
    {
      "name": "Mike Rodriguez",
      "role": "Engineering Manager",
      "team": "Backend Authentication Team",
      "email": "mike.rodriguez@company.com",
      "slack_handle": "@mike.r",
      "expertise": ["Leadership", "Authentication", "System Design", "Mentoring", "Agile"],
      "bio": "12 years in engineering with 4 years in management. Passionate about building strong teams and secure systems.",
      "location": "San Francisco, CA",
      "timezone": "PST",
      "availability": "Generally available 8 AM - 6 PM PST",
      "fun_fact": "Former startup founder and mentor at local accelerator"
    },
    {
      "name": "Jennifer Liu",
      "role": "Engineering Manager",
      "team": "Payments Team",
      "email": "jennifer.liu@company.com",
      "slack_handle": "@jennifer.liu",
      "expertise": ["Payment Systems", "Team Leadership", "Compliance", "Risk Management"],
      "bio": "15 years in fintech and payments. Expert in payment regulations and building compliant systems.",
      "location": "New York, NY",
      "timezone": "EST",
      "availability": "Available 9 AM - 6 PM EST",
      "fun_fact": "Fluent in 4 languages and loves international travel"
    }
  ]
}'::jsonb);

-- Team Structure
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('teams', 'structure', 'team_structure.json', 'team_info', '{
  "organization_structure": {
    "company": "TechCorp Solutions",
    "engineering_org": {
      "vp_engineering": "Sarah Mitchell",
      "departments": [
        "Backend Engineering",
        "Frontend Engineering",
        "Infrastructure & DevOps",
        "Data Engineering",
        "Security Engineering",
        "Quality Assurance"
      ]
    }
  },
  "teams": {
    "Backend Authentication Team": {
      "description": "Responsible for authentication, authorization, and user identity services",
      "manager": "Mike Rodriguez",
      "members": [
        {
          "name": "Mike Rodriguez",
          "role": "Engineering Manager",
          "email": "mike.rodriguez@company.com"
        },
        {
          "name": "Alice Chen",
          "role": "Senior Backend Engineer",
          "email": "alice.chen@company.com"
        },
        {
          "name": "Bob Johnson",
          "role": "Backend Engineer",
          "email": "bob.johnson@company.com"
        },
        {
          "name": "Carol White",
          "role": "Backend Engineer",
          "email": "carol.white@company.com"
        },
        {
          "name": "David Lee",
          "role": "Junior Backend Engineer",
          "email": "david.lee@company.com"
        }
      ],
      "focus_areas": [
        "JWT token management",
        "OAuth2 integration",
        "Session management",
        "Security protocols",
        "User authentication"
      ],
      "collaboration_tools": ["Slack", "Jira", "GitHub", "Confluence"],
      "meeting_schedule": {
        "daily_standup": "9:00 AM PST",
        "sprint_planning": "Monday 2:00 PM PST",
        "retrospective": "Friday 3:00 PM PST"
      },
      "key_projects": [
        "Multi-factor authentication rollout",
        "OAuth2 provider expansion",
        "Session security improvements"
      ],
      "team_culture": "Security-first mindset with focus on robust authentication solutions"
    },
    "Payments Team": {
      "description": "Handles all payment processing, fraud detection, and financial integrations",
      "manager": "Jennifer Liu",
      "members": [
        {
          "name": "Jennifer Liu",
          "role": "Engineering Manager",
          "email": "jennifer.liu@company.com"
        },
        {
          "name": "Eric Wang",
          "role": "Senior Payment Engineer",
          "email": "eric.wang@company.com"
        },
        {
          "name": "Frank Garcia",
          "role": "Payment Engineer",
          "email": "frank.garcia@company.com"
        },
        {
          "name": "Grace Kim",
          "role": "Fraud Detection Engineer",
          "email": "grace.kim@company.com"
        }
      ],
      "focus_areas": [
        "Payment gateway integration",
        "Fraud detection ML models",
        "PCI compliance",
        "Transaction processing",
        "Financial reporting"
      ],
      "collaboration_tools": ["Slack", "Jira", "GitHub", "Datadog"],
      "meeting_schedule": {
        "daily_standup": "9:30 AM PST",
        "security_review": "Wednesday 2:00 PM PST",
        "sprint_planning": "Monday 10:00 AM PST"
      },
      "key_projects": [
        "New payment provider integration",
        "Real-time fraud detection system",
        "Payment analytics dashboard"
      ],
      "team_culture": "Detail-oriented with strong focus on security and compliance"
    },
    "Frontend Team": {
      "description": "Builds user interfaces and experiences across web and mobile platforms",
      "manager": "Rachel Green",
      "members": [
        {
          "name": "Rachel Green",
          "role": "Frontend Engineering Manager",
          "email": "rachel.green@company.com"
        },
        {
          "name": "Henry Taylor",
          "role": "Senior Frontend Engineer",
          "email": "henry.taylor@company.com"
        },
        {
          "name": "Isabel Martinez",
          "role": "Frontend Engineer",
          "email": "isabel.martinez@company.com"
        },
        {
          "name": "Jack Wilson",
          "role": "UI/UX Engineer",
          "email": "jack.wilson@company.com"
        },
        {
          "name": "Kelly Brown",
          "role": "Mobile Engineer",
          "email": "kelly.brown@company.com"
        }
      ],
      "focus_areas": [
        "React development",
        "Mobile app development",
        "Performance optimization",
        "Accessibility",
        "Design systems"
      ],
      "collaboration_tools": ["Slack", "Figma", "GitHub", "Storybook"],
      "meeting_schedule": {
        "daily_standup": "10:00 AM PST",
        "design_review": "Tuesday 2:00 PM PST",
        "sprint_planning": "Monday 3:00 PM PST"
      },
      "key_projects": [
        "Design system 2.0",
        "Mobile app redesign",
        "Performance improvements initiative"
      ],
      "team_culture": "User-focused with emphasis on clean, performant interfaces"
    },
    "Infrastructure Team": {
      "description": "Manages cloud infrastructure, DevOps, and platform reliability",
      "manager": "David Kim",
      "members": [
        {
          "name": "David Kim",
          "role": "Infrastructure Manager",
          "email": "david.kim@company.com"
        },
        {
          "name": "Laura Anderson",
          "role": "Senior DevOps Engineer",
          "email": "laura.anderson@company.com"
        },
        {
          "name": "Mark Thompson",
          "role": "Site Reliability Engineer",
          "email": "mark.thompson@company.com"
        },
        {
          "name": "Nancy Davis",
          "role": "Cloud Architect",
          "email": "nancy.davis@company.com"
        }
      ],
      "focus_areas": [
        "Kubernetes management",
        "CI/CD pipelines",
        "Infrastructure as Code",
        "Monitoring and alerting",
        "Cost optimization"
      ],
      "collaboration_tools": ["Slack", "PagerDuty", "Terraform", "Prometheus"],
      "meeting_schedule": {
        "daily_standup": "8:30 AM PST",
        "incident_review": "Friday 2:00 PM PST",
        "capacity_planning": "Monthly, first Tuesday"
      },
      "key_projects": [
        "Multi-region deployment",
        "Kubernetes upgrade",
        "Disaster recovery improvements"
      ],
      "team_culture": "Reliability-focused with strong automation and monitoring practices"
    },
    "Data Engineering Team": {
      "description": "Builds data pipelines, analytics infrastructure, and ML platforms",
      "manager": "Alex Thompson",
      "members": [
        {
          "name": "Alex Thompson",
          "role": "Data Engineering Manager",
          "email": "alex.thompson@company.com"
        },
        {
          "name": "Olivia Parker",
          "role": "Senior Data Engineer",
          "email": "olivia.parker@company.com"
        },
        {
          "name": "Peter Zhang",
          "role": "ML Engineer",
          "email": "peter.zhang@company.com"
        },
        {
          "name": "Quinn Roberts",
          "role": "Data Platform Engineer",
          "email": "quinn.roberts@company.com"
        }
      ],
      "focus_areas": [
        "Data pipeline development",
        "Real-time streaming",
        "ML model deployment",
        "Data warehouse management",
        "Analytics infrastructure"
      ],
      "collaboration_tools": ["Slack", "Airflow", "BigQuery", "Jupyter"],
      "meeting_schedule": {
        "daily_standup": "9:00 AM PST",
        "data_quality_review": "Thursday 2:00 PM PST",
        "architecture_review": "Bi-weekly Wednesday"
      },
      "key_projects": [
        "Real-time analytics platform",
        "ML feature store",
        "Data quality monitoring system"
      ],
      "team_culture": "Data-driven with focus on scalable, reliable data infrastructure"
    }
  }
}'::jsonb);

-- Team Scheduling
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('teams', 'scheduling', 'scheduling.json', 'team_info', '{
  "default_slots": [
    {
      "day": "Today",
      "slots": ["2:00 PM - 2:30 PM", "3:30 PM - 4:00 PM", "4:30 PM - 5:00 PM"]
    },
    {
      "day": "Tomorrow", 
      "slots": ["10:00 AM - 10:30 AM", "11:00 AM - 11:30 AM", "2:00 PM - 2:30 PM", "3:00 PM - 3:30 PM"]
    },
    {
      "day": "Day after tomorrow",
      "slots": ["9:00 AM - 9:30 AM", "10:30 AM - 11:00 AM", "1:00 PM - 1:30 PM", "4:00 PM - 4:30 PM"]
    }
  ],
  "meeting_tips": {
    "introduction": [
      "Prepare a brief introduction about your background",
      "Share what brought you to the company",
      "Ask about their role and current projects",
      "Discuss how you might collaborate"
    ],
    "help": [
      "Come prepared with specific questions",
      "Share what you''ve already tried",
      "Bring any relevant code or error messages",
      "Take notes during the discussion"
    ],
    "1:1": [
      "Discuss your goals and expectations",
      "Ask for feedback on your progress",
      "Share any blockers or challenges",
      "Plan next steps and action items"
    ],
    "technical": [
      "Prepare technical context beforehand",
      "Have your development environment ready",
      "Share screens if discussing code",
      "Document decisions and next steps"
    ],
    "onboarding": [
      "Ask about team processes and workflows",
      "Understand team priorities and goals",
      "Learn about communication preferences",
      "Get recommendations for learning resources"
    ]
  },
  "meeting_etiquette": {
    "before_meeting": [
      "Send agenda or topics in advance",
      "Test your audio/video setup",
      "Review any relevant documentation",
      "Prepare questions or discussion points"
    ],
    "during_meeting": [
      "Join on time or a minute early",
      "Introduce yourself if meeting new people",
      "Stay engaged and ask questions",
      "Take notes of important points"
    ],
    "after_meeting": [
      "Send follow-up with action items",
      "Share any promised resources",
      "Schedule follow-up meetings if needed",
      "Update relevant documentation"
    ]
  },
  "calendar_integration": {
    "google_calendar": {
      "enabled": true,
      "instructions": "Use your @company.com Google account to access calendars"
    },
    "outlook": {
      "enabled": false,
      "instructions": "Outlook integration coming soon"
    }
  }
}'::jsonb);

-- 2. CODEBASE DATA
-- ============================================================================

-- Repositories
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('codebase', 'repositories', 'repositories.json', 'code_info', '{
  "repositories": [
    {
      "name": "user-auth-service",
      "description": "Comprehensive user authentication and authorization service with JWT tokens, OAuth2, and role-based access control",
      "language": "Python",
      "framework": "FastAPI",
      "key_files": [
        "auth/models.py",
        "auth/routes.py",
        "auth/utils.py",
        "auth/middleware.py",
        "auth/oauth.py"
      ],
      "dependencies": ["postgresql", "redis", "jwt", "oauth2", "passlib", "python-jose"],
      "team": "Backend Authentication Team",
      "documentation": "Well documented with OpenAPI specs and integration examples",
      "examples": {
        "login": "POST /auth/login with username/password",
        "verify": "GET /auth/verify with Authorization header",
        "refresh": "POST /auth/refresh with refresh token",
        "oauth": "GET /auth/oauth/google for Google OAuth flow"
      }
    },
    {
      "name": "payment-gateway",
      "description": "Multi-provider payment processing system supporting Stripe, PayPal, and bank transfers with fraud detection",
      "language": "Python",
      "framework": "Django",
      "key_files": [
        "payments/processors.py",
        "payments/models.py",
        "payments/webhooks.py",
        "payments/fraud_detection.py"
      ],
      "dependencies": ["stripe", "paypal-api", "celery", "redis", "django-rest-framework"],
      "team": "Payments Team",
      "documentation": "Includes integration guides, webhook examples, and fraud prevention docs"
    },
    {
      "name": "user-management-api",
      "description": "RESTful API for user profile management, preferences, and account settings",
      "language": "Node.js",
      "framework": "Express",
      "key_files": [
        "routes/users.js",
        "controllers/userController.js",
        "models/User.js",
        "middleware/validation.js"
      ],
      "dependencies": ["express", "mongoose", "joi", "bcrypt", "jsonwebtoken"],
      "team": "Backend User Team",
      "documentation": "Swagger documentation with examples"
    },
    {
      "name": "frontend-dashboard",
      "description": "React-based admin dashboard for managing users, payments, and analytics",
      "language": "JavaScript",
      "framework": "React",
      "key_files": [
        "src/components/Dashboard.jsx",
        "src/services/api.js",
        "src/hooks/useAuth.js",
        "src/utils/permissions.js"
      ],
      "dependencies": ["react", "redux", "axios", "material-ui", "recharts"],
      "team": "Frontend Team",
      "documentation": "Component library and styling guide available"
    },
    {
      "name": "notification-service",
      "description": "Microservice handling email, SMS, and push notifications with template management",
      "language": "Python",
      "framework": "Flask",
      "key_files": [
        "notifications/email_sender.py",
        "notifications/sms_sender.py",
        "notifications/push_notifications.py",
        "templates/template_manager.py"
      ],
      "dependencies": ["sendgrid", "twilio", "firebase-admin", "jinja2"],
      "team": "Infrastructure Team",
      "documentation": "API docs and template creation guide"
    },
    {
      "name": "data-analytics-pipeline",
      "description": "Real-time data processing pipeline for user behavior analytics and reporting",
      "language": "Python",
      "framework": "Apache Beam",
      "key_files": [
        "pipelines/user_events.py",
        "pipelines/aggregations.py",
        "transforms/enrichment.py",
        "sinks/bigquery_sink.py"
      ],
      "dependencies": ["apache-beam", "google-cloud-bigquery", "google-cloud-pubsub"],
      "team": "Data Engineering Team",
      "documentation": "Pipeline architecture and data flow documentation"
    }
  ],
  "code_snippets": {
    "authentication": {
      "file": "auth/models.py",
      "function": "authenticate_user",
      "code": "def authenticate_user(username: str, password: str) -> Optional[User]:\\n    \"\"\"Authenticate user with username and password\"\"\"\\n    user = User.query.filter_by(username=username).first()\\n    if user and user.check_password(password):\\n        # Log successful authentication\\n        logger.info(f''Successful login for user: {username}'')\\n        return user\\n    logger.warning(f''Failed login attempt for user: {username}'')\\n    return None",
      "description": "Main authentication function with password verification and logging",
      "best_practices": ["Uses bcrypt for password hashing", "Implements rate limiting", "Logs authentication attempts", "Returns user object on success"]
    },
    "payment_processing": {
      "file": "payments/processors.py",
      "function": "process_payment",
      "code": "async def process_payment(payment_data: PaymentRequest) -> PaymentResult:\\n    \"\"\"Process payment through configured provider\"\"\"\\n    provider = get_payment_provider(payment_data.provider)\\n    \\n    try:\\n        result = await provider.charge(\\n            amount=payment_data.amount,\\n            currency=payment_data.currency,\\n            source=payment_data.source\\n        )\\n        \\n        # Record transaction\\n        await Transaction.create(\\n            payment_id=result.id,\\n            amount=payment_data.amount,\\n            status=''completed''\\n        )\\n        \\n        return PaymentResult(success=True, transaction_id=result.id)\\n    except PaymentError as e:\\n        logger.error(f''Payment failed: {e}'')\\n        return PaymentResult(success=False, error=str(e))",
      "description": "Async payment processing with error handling and transaction recording",
      "best_practices": ["Async/await for I/O operations", "Proper error handling", "Transaction logging", "Type hints for clarity"]
    },
    "api_middleware": {
      "file": "middleware/auth.js",
      "function": "verifyToken",
      "code": "const verifyToken = async (req, res, next) => {\\n  const token = req.headers.authorization?.split('' '')[1];\\n  \\n  if (!token) {\\n    return res.status(401).json({ error: ''No token provided'' });\\n  }\\n  \\n  try {\\n    const decoded = jwt.verify(token, process.env.JWT_SECRET);\\n    req.user = await User.findById(decoded.userId);\\n    next();\\n  } catch (error) {\\n    return res.status(403).json({ error: ''Invalid token'' });\\n  }\\n};",
      "description": "JWT token verification middleware for Express",
      "best_practices": ["Extracts token from Authorization header", "Validates JWT signature", "Attaches user to request", "Proper error responses"]
    }
  }
}'::jsonb);

-- Dependencies
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('codebase', 'dependencies', 'dependencies.json', 'code_info', '{
  "modules": {
    "user-auth-service": {
      "description": "Authentication and authorization service",
      "architecture_layer": "service",
      "dependencies": ["postgresql", "redis", "user-management-api"],
      "dependents": ["frontend-dashboard", "payment-gateway", "notification-service"],
      "communication_methods": ["REST API", "JWT tokens", "WebSocket"],
      "data_flows": [
        "Receives login requests from frontend",
        "Validates credentials against user database",
        "Issues JWT tokens for authenticated sessions",
        "Provides user authorization info to other services"
      ],
      "integration_points": [
        "Database: PostgreSQL for user storage",
        "Cache: Redis for session management",
        "API: REST endpoints for authentication",
        "Security: JWT token validation middleware"
      ]
    },
    "payment-gateway": {
      "description": "Payment processing and financial transactions",
      "architecture_layer": "service",
      "dependencies": ["user-auth-service", "notification-service", "fraud-detection-ml"],
      "dependents": ["frontend-dashboard", "billing-service", "reporting-service"],
      "communication_methods": ["REST API", "Webhooks", "Message Queue"],
      "data_flows": [
        "Receives payment requests from frontend",
        "Validates user authorization with auth service",
        "Processes payments through external providers",
        "Sends payment confirmations via notification service"
      ],
      "integration_points": [
        "External APIs: Stripe, PayPal integration",
        "Queue: Celery for async processing",
        "Webhooks: Payment provider callbacks",
        "Database: Transaction logging"
      ]
    },
    "frontend-dashboard": {
      "description": "React-based user interface for admin operations",
      "architecture_layer": "presentation",
      "dependencies": ["user-auth-service", "user-management-api", "payment-gateway", "notification-service"],
      "dependents": [],
      "communication_methods": ["HTTP requests", "WebSocket connections", "Server-sent events"],
      "data_flows": [
        "Authenticates users through auth service",
        "Fetches user data from management API",
        "Displays payment information from gateway",
        "Sends admin actions to backend services"
      ],
      "integration_points": [
        "Authentication: JWT token management",
        "API calls: Axios for HTTP requests",
        "State management: Redux for app state",
        "UI components: Material-UI library"
      ]
    },
    "notification-service": {
      "description": "Multi-channel notification delivery system",
      "architecture_layer": "service",
      "dependencies": ["user-management-api", "template-engine", "message-queue"],
      "dependents": ["payment-gateway", "user-auth-service", "order-service"],
      "communication_methods": ["Message Queue", "REST API", "gRPC"],
      "data_flows": [
        "Receives notification requests from services",
        "Fetches user preferences from management API",
        "Renders messages using template engine",
        "Delivers via email, SMS, or push notifications"
      ],
      "integration_points": [
        "Email: SendGrid for email delivery",
        "SMS: Twilio for text messages",
        "Push: Firebase for mobile notifications",
        "Queue: Redis for message processing"
      ]
    },
    "user-management-api": {
      "description": "User profile and account management",
      "architecture_layer": "service",
      "dependencies": ["mongodb", "redis-cache", "elasticsearch"],
      "dependents": ["frontend-dashboard", "notification-service", "analytics-service"],
      "communication_methods": ["REST API", "GraphQL", "Event streaming"],
      "data_flows": [
        "Manages user profile data",
        "Handles preference updates",
        "Provides user search capabilities",
        "Syncs data with analytics service"
      ],
      "integration_points": [
        "Database: MongoDB for user data",
        "Cache: Redis for performance",
        "Search: Elasticsearch for user search",
        "API: REST and GraphQL endpoints"
      ]
    },
    "data-analytics-pipeline": {
      "description": "Real-time data processing and analytics",
      "architecture_layer": "data",
      "dependencies": ["pubsub", "bigquery", "dataflow"],
      "dependents": ["reporting-dashboard", "ml-models"],
      "communication_methods": ["Pub/Sub", "Streaming", "Batch processing"],
      "data_flows": [
        "Ingests events from all services",
        "Processes and aggregates data in real-time",
        "Stores results in BigQuery",
        "Feeds ML models with processed data"
      ],
      "integration_points": [
        "Ingestion: Cloud Pub/Sub for events",
        "Processing: Apache Beam pipelines",
        "Storage: BigQuery data warehouse",
        "Output: Reporting APIs"
      ]
    }
  }
}'::jsonb);

-- Tech Stack
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('codebase', 'tech_stack', 'tech_stack.json', 'code_info', '{
  "overview": "Modern microservices architecture with cloud-native technologies",
  "frontend": {
    "react": {
      "version": "18.2.0",
      "description": "Main frontend framework for web applications",
      "usage": ["Admin dashboard", "Customer portal", "Internal tools"],
      "related_tools": ["Redux", "React Router", "Material-UI"]
    },
    "nextjs": {
      "version": "13.4.0",
      "description": "Server-side rendering framework for public-facing pages",
      "usage": ["Marketing website", "Documentation site", "Blog"],
      "features": ["SSR", "Static generation", "API routes"]
    },
    "mobile": {
      "react_native": {
        "version": "0.72.0",
        "description": "Cross-platform mobile development",
        "platforms": ["iOS", "Android"],
        "usage": ["Customer mobile app", "Field service app"]
      }
    }
  },
  "backend": {
    "python": {
      "frameworks": {
        "fastapi": {
          "version": "0.104.0",
          "description": "Modern async web framework",
          "usage": ["Authentication service", "API gateway", "Microservices"]
        },
        "django": {
          "version": "4.2.0",
          "description": "Full-featured web framework",
          "usage": ["Payment gateway", "Admin interfaces", "CMS"]
        },
        "flask": {
          "version": "3.0.0",
          "description": "Lightweight web framework",
          "usage": ["Notification service", "Webhooks", "Simple APIs"]
        }
      }
    },
    "nodejs": {
      "frameworks": {
        "express": {
          "version": "4.18.0",
          "description": "Web application framework",
          "usage": ["User management API", "Real-time services", "GraphQL server"]
        },
        "nestjs": {
          "version": "10.2.0",
          "description": "Enterprise-grade Node.js framework",
          "usage": ["Microservices", "Event-driven services"]
        }
      }
    },
    "java": {
      "frameworks": {
        "spring_boot": {
          "version": "3.1.0",
          "description": "Enterprise Java framework",
          "usage": ["Legacy services", "Enterprise integrations", "Batch processing"]
        }
      }
    }
  },
  "infrastructure": {
    "cloud_provider": "Google Cloud Platform",
    "container_orchestration": {
      "kubernetes": {
        "version": "1.28",
        "description": "Container orchestration platform",
        "usage": ["All microservices", "Auto-scaling", "Service mesh"]
      }
    },
    "service_mesh": {
      "istio": {
        "version": "1.19",
        "description": "Service mesh for microservices",
        "features": ["Traffic management", "Security", "Observability"]
      }
    },
    "ci_cd": {
      "github_actions": {
        "description": "CI/CD pipeline automation",
        "usage": ["Build", "Test", "Deploy", "Release automation"]
      },
      "argocd": {
        "version": "2.8",
        "description": "GitOps continuous delivery",
        "usage": ["Kubernetes deployments", "Configuration management"]
      }
    }
  },
  "databases": {
    "postgresql": {
      "version": "15.4",
      "description": "Primary relational database",
      "usage": ["User data", "Transactions", "Core business data"],
      "features": ["ACID compliance", "JSON support", "Full-text search"]
    },
    "mongodb": {
      "version": "7.0",
      "description": "Document database",
      "usage": ["User profiles", "Content management", "Flexible schemas"],
      "features": ["Aggregation pipeline", "Change streams", "Sharding"]
    },
    "redis": {
      "version": "7.2",
      "description": "In-memory data structure store",
      "usage": ["Caching", "Session storage", "Real-time features"],
      "features": ["Pub/Sub", "Lua scripting", "Persistence options"]
    },
    "elasticsearch": {
      "version": "8.10",
      "description": "Search and analytics engine",
      "usage": ["Full-text search", "Log analytics", "Application monitoring"],
      "features": ["RESTful API", "Aggregations", "Machine learning"]
    },
    "bigquery": {
      "description": "Data warehouse for analytics",
      "usage": ["Business intelligence", "Data analytics", "ML datasets"],
      "features": ["Serverless", "Real-time analytics", "ML integration"]
    }
  },
  "tools": {
    "monitoring": {
      "prometheus": {
        "description": "Metrics collection and alerting",
        "usage": ["Service metrics", "System monitoring", "Custom metrics"]
      },
      "grafana": {
        "description": "Metrics visualization",
        "usage": ["Dashboards", "Alerting", "Data exploration"]
      },
      "elastic_stack": {
        "description": "Logging and observability",
        "components": ["Elasticsearch", "Logstash", "Kibana", "Beats"]
      }
    },
    "message_queue": {
      "rabbitmq": {
        "version": "3.12",
        "description": "Message broker",
        "usage": ["Async processing", "Event-driven architecture", "Task queues"]
      },
      "kafka": {
        "version": "3.5",
        "description": "Distributed streaming platform",
        "usage": ["Event streaming", "Data pipelines", "Real-time processing"]
      }
    },
    "api_gateway": {
      "kong": {
        "version": "3.4",
        "description": "API gateway and management",
        "features": ["Rate limiting", "Authentication", "Load balancing"]
      }
    }
  }
}'::jsonb);

-- Best Practices
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('codebase', 'best_practices', 'best_practices.json', 'code_info', '{
  "general": {
    "guidelines": [
      "Use clear, descriptive variable and function names",
      "Write comprehensive docstrings for all functions and classes",
      "Implement proper error handling and logging",
      "Follow the DRY principle (Don''t Repeat Yourself)",
      "Use type hints for better code clarity",
      "Keep functions focused on a single responsibility",
      "Write unit tests for all business logic",
      "Document complex algorithms and business rules"
    ]
  },
  "languages": {
    "python": {
      "guidelines": [
        "Follow PEP 8 style guidelines",
        "Use virtual environments for dependency management",
        "Implement proper exception handling with specific exception types",
        "Use f-strings for string formatting",
        "Leverage list/dict comprehensions when appropriate",
        "Use asyncio for I/O-bound operations",
        "Type hints for all function parameters and returns",
        "Use dataclasses for data structures"
      ]
    },
    "javascript": {
      "guidelines": [
        "Use const/let instead of var",
        "Implement proper error boundaries in React",
        "Use async/await for asynchronous operations",
        "Follow ESLint rules for consistent code style",
        "Use TypeScript for large applications",
        "Implement proper state management patterns",
        "Avoid callback hell with promises",
        "Use destructuring for cleaner code"
      ]
    },
    "java": {
      "guidelines": [
        "Follow Google Java Style Guide",
        "Use dependency injection frameworks",
        "Implement proper exception handling",
        "Use Optional for nullable values",
        "Leverage streams for collections",
        "Follow SOLID principles",
        "Use meaningful package structure",
        "Document with Javadoc"
      ]
    }
  },
  "quality_checklist": [
    "Code has comprehensive test coverage (>80%)",
    "All functions have proper documentation",
    "Error handling is implemented consistently",
    "Security best practices are followed",
    "Performance considerations are addressed",
    "Code review has been completed",
    "No hardcoded values or credentials",
    "Logging is implemented appropriately"
  ],
  "rules": [
    {
      "trigger": "password",
      "type": "recommendation",
      "rule": "Password Security",
      "message": "Ensure passwords are hashed using bcrypt or similar secure algorithm",
      "improvement": "Never store passwords in plain text, use proper hashing"
    },
    {
      "trigger": "todo",
      "type": "violation",
      "rule": "Code Comments",
      "message": "TODO comments should be removed before production",
      "severity": "low"
    },
    {
      "trigger": "print(",
      "type": "violation",
      "rule": "Logging Standards",
      "message": "Use proper logging instead of print statements",
      "severity": "medium"
    },
    {
      "trigger": "except:",
      "type": "violation",
      "rule": "Exception Handling",
      "message": "Avoid bare except clauses - catch specific exceptions",
      "severity": "high"
    },
    {
      "trigger": "sql",
      "type": "recommendation",
      "rule": "SQL Security",
      "message": "Use parameterized queries to prevent SQL injection",
      "improvement": "Never concatenate user input into SQL queries"
    },
    {
      "trigger": "api_key",
      "type": "violation",
      "rule": "Security",
      "message": "API keys should not be hardcoded in source code",
      "severity": "critical"
    },
    {
      "trigger": "http://",
      "type": "recommendation",
      "rule": "Security",
      "message": "Use HTTPS for all external connections",
      "improvement": "Replace http:// with https:// for security"
    }
  ]
}'::jsonb);

-- 3. DOCUMENTATION DATA
-- ============================================================================

-- API Documentation
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('documentation', 'api', 'api_docs.json', 'doc_info', '{
  "apis": [
    {
      "name": "Authentication API",
      "description": "User authentication and authorization service",
      "version": "v2.1",
      "base_url": "https://api.company.com/auth",
      "documentation_url": "https://docs.company.com/auth-api",
      "status": "stable",
      "authentication": {
        "type": "Bearer Token",
        "description": "Include JWT token in Authorization header"
      },
      "key_endpoints": [
        {
          "method": "POST",
          "path": "/login",
          "description": "Authenticate user with username/password",
          "parameters": ["username", "password"],
          "response": "JWT access token and refresh token"
        },
        {
          "method": "POST",
          "path": "/refresh",
          "description": "Refresh access token using refresh token",
          "parameters": ["refresh_token"],
          "response": "New JWT access token"
        },
        {
          "method": "GET",
          "path": "/verify",
          "description": "Verify JWT token validity",
          "parameters": ["Authorization header"],
          "response": "User info and token status"
        },
        {
          "method": "POST",
          "path": "/logout",
          "description": "Invalidate user session and tokens",
          "parameters": ["Authorization header"],
          "response": "Logout confirmation"
        },
        {
          "method": "GET",
          "path": "/oauth/{provider}",
          "description": "Initiate OAuth flow with provider",
          "parameters": ["provider"],
          "response": "OAuth redirect URL"
        }
      ]
    },
    {
      "name": "Payment Gateway API",
      "description": "Payment processing and transaction management",
      "version": "v1.3",
      "base_url": "https://api.company.com/payments",
      "documentation_url": "https://docs.company.com/payment-api",
      "status": "stable",
      "authentication": {
        "type": "API Key + Bearer Token",
        "description": "Requires both API key and user JWT token"
      },
      "key_endpoints": [
        {
          "method": "POST",
          "path": "/charge",
          "description": "Process a payment charge",
          "parameters": ["amount", "currency", "payment_method", "customer_id"],
          "response": "Transaction ID and status"
        },
        {
          "method": "GET",
          "path": "/transactions/{id}",
          "description": "Get transaction details",
          "parameters": ["transaction_id"],
          "response": "Complete transaction information"
        },
        {
          "method": "POST",
          "path": "/refund",
          "description": "Process a refund for existing transaction",
          "parameters": ["transaction_id", "amount", "reason"],
          "response": "Refund confirmation and ID"
        },
        {
          "method": "POST",
          "path": "/webhooks/configure",
          "description": "Configure webhook endpoints",
          "parameters": ["url", "events"],
          "response": "Webhook configuration"
        }
      ]
    },
    {
      "name": "User Management API",
      "description": "User profile and account management",
      "version": "v1.8",
      "base_url": "https://api.company.com/users",
      "documentation_url": "https://docs.company.com/user-api",
      "status": "stable",
      "authentication": {
        "type": "Bearer Token",
        "description": "JWT token required for all endpoints"
      },
      "key_endpoints": [
        {
          "method": "GET",
          "path": "/profile",
          "description": "Get current user profile",
          "parameters": ["Authorization header"],
          "response": "User profile data"
        },
        {
          "method": "PUT",
          "path": "/profile",
          "description": "Update user profile information",
          "parameters": ["profile data object"],
          "response": "Updated profile confirmation"
        },
        {
          "method": "GET",
          "path": "/preferences",
          "description": "Get user notification and app preferences",
          "parameters": ["Authorization header"],
          "response": "User preferences object"
        },
        {
          "method": "POST",
          "path": "/search",
          "description": "Search for users",
          "parameters": ["query", "filters"],
          "response": "List of matching users"
        }
      ]
    },
    {
      "name": "Notification API",
      "description": "Multi-channel notification delivery service",
      "version": "v2.0",
      "base_url": "https://api.company.com/notifications",
      "documentation_url": "https://docs.company.com/notification-api",
      "status": "stable",
      "authentication": {
        "type": "Service Token",
        "description": "Service-to-service authentication token"
      },
      "key_endpoints": [
        {
          "method": "POST",
          "path": "/send",
          "description": "Send notification to user",
          "parameters": ["user_id", "channel", "template", "data"],
          "response": "Notification ID and status"
        },
        {
          "method": "GET",
          "path": "/templates",
          "description": "List available notification templates",
          "parameters": ["channel"],
          "response": "List of templates"
        },
        {
          "method": "GET",
          "path": "/status/{id}",
          "description": "Check notification delivery status",
          "parameters": ["notification_id"],
          "response": "Delivery status and metadata"
        }
      ]
    }
  ]
}'::jsonb);

-- Tutorials
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('documentation', 'tutorials', 'tutorials.json', 'doc_info', '{
  "tutorials": [
    {
      "title": "Setting Up Your Development Environment",
      "description": "Complete guide to setting up local development environment with all required tools and configurations",
      "difficulty": "beginner",
      "estimated_time": "30 minutes",
      "url": "/tutorials/dev-environment-setup",
      "topics": ["environment", "setup", "tools", "configuration"]
    },
    {
      "title": "Working with Our Authentication System",
      "description": "Learn how to integrate with our auth system, handle JWT tokens, and implement proper security",
      "difficulty": "intermediate",
      "estimated_time": "45 minutes",
      "url": "/tutorials/authentication-integration",
      "topics": ["authentication", "jwt", "security", "integration"]
    },
    {
      "title": "Payment Integration Best Practices",
      "description": "How to safely integrate payment processing with proper error handling and security measures",
      "difficulty": "advanced",
      "estimated_time": "60 minutes",
      "url": "/tutorials/payment-integration",
      "topics": ["payments", "security", "error-handling", "compliance"]
    },
    {
      "title": "Database Operations and Migrations",
      "description": "Working with our database, creating migrations, and following data access patterns",
      "difficulty": "intermediate",
      "estimated_time": "40 minutes",
      "url": "/tutorials/database-operations",
      "topics": ["database", "migrations", "sql", "data-access"]
    },
    {
      "title": "Testing Strategies and Frameworks",
      "description": "Writing effective tests for our codebase using our testing frameworks and best practices",
      "difficulty": "intermediate",
      "estimated_time": "50 minutes",
      "url": "/tutorials/testing-guide",
      "topics": ["testing", "unit-tests", "integration-tests", "mocking"]
    },
    {
      "title": "Deployment and Release Process",
      "description": "Understanding our CI/CD pipeline, deployment procedures, and release management",
      "difficulty": "advanced",
      "estimated_time": "35 minutes",
      "url": "/tutorials/deployment-process",
      "topics": ["deployment", "cicd", "releases", "production"]
    },
    {
      "title": "Building RESTful APIs",
      "description": "Guidelines for designing and implementing RESTful APIs following our standards",
      "difficulty": "intermediate",
      "estimated_time": "40 minutes",
      "url": "/tutorials/restful-api-design",
      "topics": ["api", "rest", "design", "standards"]
    },
    {
      "title": "Microservices Development Guide",
      "description": "Best practices for developing microservices in our architecture",
      "difficulty": "advanced",
      "estimated_time": "55 minutes",
      "url": "/tutorials/microservices-guide",
      "topics": ["microservices", "architecture", "design-patterns", "communication"]
    }
  ]
}'::jsonb);

-- Wiki Pages
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('documentation', 'wiki', 'wiki_pages.json', 'doc_info', '{
  "pages": [
    {
      "title": "Getting Started - New Developer Guide",
      "url": "/wiki/getting-started",
      "summary": "Complete guide for new developers including environment setup, code conventions, and team processes",
      "content": "Welcome to our development team! This guide covers everything you need to know to get productive quickly. Topics include: development environment setup, coding standards, git workflow, testing practices, and team communication tools.",
      "last_updated": "2024-12-15",
      "author": "Sarah Chen",
      "tags": ["onboarding", "development", "setup", "new-hire"]
    },
    {
      "title": "Authentication System Architecture",
      "url": "/wiki/auth-architecture",
      "summary": "Deep dive into our authentication and authorization system design",
      "content": "Our authentication system uses JWT tokens with refresh token rotation. The system supports OAuth2 for third-party authentication and implements role-based access control (RBAC). Key components include: JWT token service, OAuth2 provider integration, role management, and session handling.",
      "last_updated": "2024-11-20",
      "author": "Mike Rodriguez",
      "tags": ["authentication", "security", "architecture", "jwt", "oauth"]
    },
    {
      "title": "Payment Processing Best Practices",
      "url": "/wiki/payment-best-practices",
      "summary": "Security and compliance guidelines for payment processing",
      "content": "When handling payments, always follow PCI DSS compliance requirements. Never store credit card numbers in logs or databases. Use tokenization for sensitive data. Implement proper error handling for failed transactions and always validate payment amounts server-side.",
      "last_updated": "2024-12-01",
      "author": "Jennifer Liu",
      "tags": ["payments", "security", "compliance", "pci-dss"]
    },
    {
      "title": "Deployment Pipeline Guide",
      "url": "/wiki/deployment-pipeline",
      "summary": "How our CI/CD pipeline works and deployment procedures",
      "content": "Our deployment pipeline uses GitHub Actions for CI/CD. Code flows through: development → staging → production. Each environment has automated tests, security scans, and deployment validation. Production deployments require two approvals and can be rolled back automatically.",
      "last_updated": "2024-11-28",
      "author": "David Kim",
      "tags": ["deployment", "cicd", "devops", "pipeline"]
    },
    {
      "title": "Database Migration Guide",
      "url": "/wiki/database-migrations",
      "summary": "How to create and run database schema changes safely",
      "content": "Database migrations must be backward compatible and tested thoroughly. Always create migration scripts in the migrations/ directory. Run migrations in staging first, then production during maintenance windows. Include rollback scripts for major changes.",
      "last_updated": "2024-12-10",
      "author": "Alex Thompson",
      "tags": ["database", "migrations", "schema", "production"]
    },
    {
      "title": "Microservices Communication Patterns",
      "url": "/wiki/microservices-patterns",
      "summary": "Best practices for inter-service communication",
      "content": "Our microservices communicate using REST APIs, gRPC, and message queues. Synchronous calls use circuit breakers and retries. Asynchronous communication uses RabbitMQ or Kafka. Service discovery is handled by Kubernetes DNS.",
      "last_updated": "2024-12-05",
      "author": "Rachel Green",
      "tags": ["microservices", "architecture", "communication", "patterns"]
    },
    {
      "title": "Monitoring and Alerting Setup",
      "url": "/wiki/monitoring-setup",
      "summary": "How to set up monitoring for your services",
      "content": "All services must expose Prometheus metrics on /metrics endpoint. Use structured logging with correlation IDs. Set up alerts for SLI violations. Dashboard templates are available in the monitoring/ directory.",
      "last_updated": "2024-11-25",
      "author": "Tom Wilson",
      "tags": ["monitoring", "observability", "prometheus", "alerting"]
    },
    {
      "title": "Security Guidelines for Developers",
      "url": "/wiki/security-guidelines",
      "summary": "Essential security practices for all developers",
      "content": "Follow OWASP Top 10 guidelines. Never commit secrets to git. Use environment variables for configuration. Implement proper input validation. Enable security headers. Use HTTPS everywhere. Regular dependency updates are mandatory.",
      "last_updated": "2024-12-12",
      "author": "Security Team",
      "tags": ["security", "guidelines", "owasp", "best-practices"]
    }
  ]
}'::jsonb);

-- 4. POLICIES DATA
-- ============================================================================

-- HR Handbook
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('policies', 'hr', 'hr_handbook.json', 'policy_info', '{
  "policies": {
    "benefits": [
      {
        "title": "Health Insurance Coverage",
        "description": "Comprehensive health insurance plans available to all full-time employees",
        "details": [
          "Medical, dental, and vision coverage included",
          "Company pays 80% of premium costs",
          "Coverage begins on first day of employment",
          "Family coverage available with employee contribution",
          "Annual open enrollment period in November",
          "HSA and FSA options available"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-11-15",
        "contact": "benefits@company.com",
        "keywords": ["health", "insurance", "medical", "dental", "vision", "hsa", "fsa"]
      },
      {
        "title": "Retirement Savings Plan (401k)",
        "description": "Company-sponsored 401k retirement savings plan with matching contributions",
        "details": [
          "Company matches 100% of first 3% contributed",
          "Additional 50% match on next 2% contributed",
          "Immediate vesting on all contributions",
          "Auto-enrollment at 6% contribution rate",
          "Can adjust contribution anytime through HR portal",
          "Roth 401k option available",
          "Annual contribution limits apply per IRS guidelines"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-10-20",
        "contact": "benefits@company.com",
        "keywords": ["401k", "retirement", "savings", "matching", "vesting"]
      },
      {
        "title": "Professional Development",
        "description": "Support for continuous learning and professional growth",
        "details": [
          "$2,500 annual budget for training and conferences",
          "20% time for learning during work hours",
          "Access to online learning platforms (Pluralsight, Coursera)",
          "Tuition reimbursement for relevant degrees",
          "Internal mentorship programs",
          "Technical certification support"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-09-15",
        "contact": "learning@company.com",
        "keywords": ["training", "development", "learning", "education", "certification"]
      }
    ],
    "leave": [
      {
        "title": "Paid Time Off (PTO) Policy",
        "description": "Flexible paid time off for vacation, personal time, and sick leave",
        "details": [
          "Accrual starts immediately upon hire",
          "New employees: 15 days PTO first year",
          "2-5 years: 20 days PTO per year",
          "5+ years: 25 days PTO per year",
          "Maximum carryover: 5 days into next year",
          "Must request PTO at least 2 weeks in advance for planned time off",
          "Unused PTO paid out upon separation"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-09-10",
        "contact": "hr@company.com",
        "keywords": ["pto", "vacation", "sick", "time off", "leave", "accrual"]
      },
      {
        "title": "Parental Leave",
        "description": "Paid leave for new parents following birth or adoption",
        "details": [
          "12 weeks paid parental leave for primary caregiver",
          "6 weeks paid leave for secondary caregiver",
          "Must be employed for 6 months to be eligible",
          "Can be taken within 12 months of birth/adoption",
          "Additional unpaid leave available under FMLA",
          "Gradual return-to-work options available",
          "Benefits continue during leave"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-08-15",
        "contact": "hr@company.com",
        "keywords": ["parental", "maternity", "paternity", "adoption", "family", "fmla"]
      },
      {
        "title": "Holidays",
        "description": "Company-observed holidays and floating holidays",
        "details": [
          "10 company holidays per year",
          "2 floating holidays to use at your discretion",
          "Holiday calendar published annually",
          "If holiday falls on weekend, observed on nearest weekday",
          "On-call employees receive comp time for holiday work"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2023-12-15",
        "contact": "hr@company.com",
        "keywords": ["holiday", "floating", "calendar", "time off"]
      }
    ],
    "conduct": [
      {
        "title": "Code of Conduct",
        "description": "Expected behavior and ethical standards for all employees",
        "details": [
          "Treat all colleagues with respect and professionalism",
          "Maintain confidentiality of company and customer information",
          "Report any conflicts of interest to management",
          "Comply with all applicable laws and regulations",
          "Use company resources responsibly",
          "Report any violations through appropriate channels",
          "No discrimination or harassment tolerated"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-12-01",
        "contact": "ethics@company.com",
        "keywords": ["conduct", "ethics", "behavior", "standards", "compliance"]
      },
      {
        "title": "Anti-Harassment Policy",
        "description": "Zero tolerance for harassment in any form",
        "details": [
          "Harassment based on any protected characteristic is prohibited",
          "Includes verbal, physical, and visual harassment",
          "Applies to all work-related settings and events",
          "Multiple reporting channels available",
          "All reports investigated promptly and confidentially",
          "Retaliation for reporting is strictly prohibited"
        ],
        "effective_date": "2024-01-01",
        "last_updated": "2024-11-01",
        "contact": "hr@company.com",
        "keywords": ["harassment", "discrimination", "reporting", "workplace"]
      }
    ],
    "remote_work": [
      {
        "title": "Remote Work Policy",
        "description": "Guidelines for working remotely and hybrid work arrangements",
        "details": [
          "Eligible after 90 days of employment",
          "Maximum 3 days remote per week for most roles",
          "Must maintain reliable internet and quiet workspace",
          "Required to attend in-person meetings when scheduled",
          "Equipment provided: laptop, monitor, desk accessories",
          "Regular check-ins with manager required",
          "$500 home office setup stipend"
        ],
        "effective_date": "2024-06-01",
        "last_updated": "2024-11-30",
        "contact": "hr@company.com",
        "keywords": ["remote", "work from home", "hybrid", "telecommute", "wfh"]
      }
    ]
  }
}'::jsonb);

-- Security Guidelines
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('policies', 'security', 'security_guidelines.json', 'policy_info', '{
  "guidelines": {
    "security": {
      "items": [
        {
          "title": "Password Security Requirements",
          "description": "Mandatory password standards for all company accounts and systems",
          "requirements": [
            "Minimum 12 characters length",
            "Must include uppercase, lowercase, numbers, and symbols",
            "Cannot reuse last 12 passwords",
            "Must change every 90 days",
            "Use multi-factor authentication where available",
            "No passwords in code or documentation"
          ],
          "best_practices": [
            "Use a password manager",
            "Enable 2FA on all accounts",
            "Never share passwords",
            "Use unique passwords for each account",
            "Use passphrases instead of passwords"
          ],
          "common_violations": [
            "Using weak or common passwords",
            "Sharing passwords with colleagues",
            "Writing passwords on sticky notes",
            "Using same password across multiple systems",
            "Storing passwords in plain text files"
          ],
          "implementation_guide": [
            "Install company-approved password manager",
            "Generate unique passwords for each account",
            "Enable 2FA using authenticator app",
            "Store recovery codes securely",
            "Regular password audits"
          ],
          "severity": "critical",
          "compliance_frameworks": ["SOC2", "ISO27001", "NIST"],
          "last_updated": "2024-11-01",
          "tags": ["passwords", "authentication", "access", "security"]
        },
        {
          "title": "Data Classification and Handling",
          "description": "Requirements for handling different types of company and customer data",
          "requirements": [
            "Classify all data according to sensitivity levels",
            "Encrypt sensitive data in transit and at rest",
            "Limit access to data based on business need",
            "Log all access to sensitive data",
            "Report data breaches within 24 hours",
            "Annual data handling training required"
          ],
          "best_practices": [
            "Use encryption for all sensitive communications",
            "Regularly review data access permissions",
            "Implement data loss prevention tools",
            "Train employees on data handling",
            "Minimize data collection and retention"
          ],
          "common_violations": [
            "Storing sensitive data in unsecured locations",
            "Sending customer data via unencrypted email",
            "Granting excessive data access permissions",
            "Not reporting suspected data breaches",
            "Keeping data longer than necessary"
          ],
          "implementation_guide": [
            "Use approved encryption tools",
            "Configure DLP policies",
            "Set up access controls",
            "Implement audit logging",
            "Create data retention policies"
          ],
          "severity": "critical",
          "compliance_frameworks": ["GDPR", "CCPA", "SOC2", "HIPAA"],
          "last_updated": "2024-10-15",
          "tags": ["data", "privacy", "encryption", "gdpr", "compliance"]
        },
        {
          "title": "Network Security",
          "description": "Requirements for secure network access and usage",
          "requirements": [
            "Use VPN for remote access",
            "No unauthorized wireless access points",
            "Segment networks by security level",
            "Monitor network traffic for anomalies",
            "Keep firewall rules up to date"
          ],
          "best_practices": [
            "Always use encrypted connections",
            "Avoid public WiFi for work",
            "Use corporate VPN consistently",
            "Report suspicious network activity",
            "Keep network diagrams current"
          ],
          "common_violations": [
            "Bypassing VPN requirements",
            "Using personal hotspots",
            "Connecting unauthorized devices",
            "Sharing WiFi passwords",
            "Ignoring security warnings"
          ],
          "severity": "high",
          "compliance_frameworks": ["SOC2", "PCI-DSS"],
          "last_updated": "2024-11-15",
          "tags": ["network", "vpn", "firewall", "security"]
        }
      ]
    },
    "development": {
      "items": [
        {
          "title": "Secure Coding Practices",
          "description": "Security requirements for software development",
          "requirements": [
            "Validate all user inputs",
            "Use parameterized queries for database operations",
            "Implement proper error handling without information disclosure",
            "Use secure authentication and session management",
            "Follow OWASP Top 10 security guidelines",
            "Security review required for all code"
          ],
          "best_practices": [
            "Conduct regular security code reviews",
            "Use static analysis security testing tools",
            "Keep dependencies updated",
            "Implement security testing in CI/CD pipeline",
            "Use secure coding checklists"
          ],
          "common_violations": [
            "SQL injection vulnerabilities",
            "Cross-site scripting (XSS) flaws",
            "Hardcoded credentials in code",
            "Insufficient input validation",
            "Exposed sensitive data in logs"
          ],
          "implementation_guide": [
            "Use ORM frameworks to prevent SQL injection",
            "Sanitize all user inputs",
            "Implement Content Security Policy headers",
            "Use environment variables for configuration",
            "Enable security linters in IDE"
          ],
          "severity": "high",
          "compliance_frameworks": ["OWASP", "NIST", "CWE"],
          "last_updated": "2024-12-01",
          "tags": ["coding", "development", "owasp", "vulnerabilities"]
        },
        {
          "title": "API Security",
          "description": "Security standards for API development and integration",
          "requirements": [
            "Implement proper authentication (OAuth2, JWT)",
            "Use HTTPS for all API endpoints",
            "Implement rate limiting",
            "Validate all input data",
            "Log all API access",
            "Version APIs properly"
          ],
          "best_practices": [
            "Use API gateways",
            "Implement request signing",
            "Monitor API usage patterns",
            "Document security requirements",
            "Regular API security testing"
          ],
          "common_violations": [
            "Exposing sensitive data in URLs",
            "Missing authentication",
            "No rate limiting",
            "Verbose error messages",
            "Insecure direct object references"
          ],
          "severity": "high",
          "compliance_frameworks": ["OWASP API", "REST Security"],
          "last_updated": "2024-11-20",
          "tags": ["api", "rest", "security", "authentication"]
        }
      ]
    },
    "operations": {
      "items": [
        {
          "title": "Access Control Management",
          "description": "Managing user access and permissions",
          "requirements": [
            "Follow principle of least privilege",
            "Regular access reviews (quarterly)",
            "Immediate revocation upon termination",
            "Document all access changes",
            "Segregation of duties for critical operations"
          ],
          "best_practices": [
            "Automate access provisioning",
            "Use role-based access control",
            "Implement approval workflows",
            "Regular permission audits",
            "Monitor privileged access"
          ],
          "common_violations": [
            "Excessive permissions",
            "Shared accounts",
            "Orphaned accounts",
            "No access reviews",
            "Manual access management"
          ],
          "severity": "critical",
          "compliance_frameworks": ["SOC2", "ISO27001"],
          "last_updated": "2024-12-05",
          "tags": ["access", "permissions", "identity", "iam"]
        }
      ]
    }
  },
  "general_principles": [
    "Security is everyone''s responsibility",
    "Defense in depth - implement multiple security layers",
    "Principle of least privilege - grant minimum required access",
    "Regular security training and awareness",
    "Incident response plan should be tested regularly",
    "Security by design - build security in from the start",
    "Assume breach - design systems to limit damage",
    "Trust but verify - audit and monitor all access"
  ]
}'::jsonb);

-- Compliance Documentation
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('policies', 'compliance', 'compliance_docs.json', 'policy_info', '{
  "regulations": {
    "GDPR": {
      "description": "General Data Protection Regulation - EU privacy regulation",
      "requirements": [
        {
          "title": "Data Subject Rights",
          "description": "Individuals have rights regarding their personal data",
          "applicable_scenarios": ["customer data", "employee data", "personal information", "user profiles"],
          "mandatory_actions": [
            "Provide clear privacy notices",
            "Enable data subject access requests",
            "Implement right to rectification",
            "Enable right to erasure (right to be forgotten)",
            "Provide data portability options",
            "Obtain explicit consent for data processing"
          ],
          "prohibited_actions": [
            "Processing personal data without legal basis",
            "Transferring data outside EU without adequate protections",
            "Retaining data longer than necessary",
            "Using data for purposes other than originally stated"
          ],
          "documentation_required": [
            "Privacy impact assessments",
            "Data processing records",
            "Consent documentation",
            "Data transfer agreements",
            "Breach notification procedures"
          ],
          "compliance_level": "critical",
          "penalties": "Up to 4% of annual global turnover or €20 million",
          "review_frequency": "annually",
          "responsible_team": "Legal and Privacy Team"
        }
      ]
    },
    "SOC2": {
      "description": "Service Organization Control 2 - Security and availability standards",
      "requirements": [
        {
          "title": "Access Controls",
          "description": "Logical and physical access controls must be implemented",
          "applicable_scenarios": ["system access", "data access", "facility access", "privileged access"],
          "mandatory_actions": [
            "Implement multi-factor authentication",
            "Regular access reviews and certifications",
            "Role-based access controls",
            "Privileged access management",
            "Access termination procedures",
            "Audit logging of all access"
          ],
          "prohibited_actions": [
            "Shared user accounts",
            "Unmonitored privileged access",
            "Backdoor access mechanisms",
            "Generic or default accounts"
          ],
          "documentation_required": [
            "Access control policies",
            "User access reviews",
            "Privileged user monitoring logs",
            "Access termination documentation",
            "Security awareness training records"
          ],
          "compliance_level": "critical",
          "penalties": "Loss of certification and customer trust",
          "review_frequency": "quarterly",
          "responsible_team": "Security and Compliance Team"
        }
      ]
    },
    "PCI_DSS": {
      "description": "Payment Card Industry Data Security Standard",
      "requirements": [
        {
          "title": "Cardholder Data Protection",
          "description": "Requirements for protecting payment card information",
          "applicable_scenarios": ["payment processing", "credit card data", "transaction handling", "payment storage"],
          "mandatory_actions": [
            "Encrypt cardholder data transmission",
            "Maintain secure network configurations",
            "Implement strong access controls",
            "Regular security testing and monitoring",
            "Maintain information security policies",
            "Use approved payment tokenization"
          ],
          "prohibited_actions": [
            "Storing sensitive authentication data",
            "Unencrypted transmission of cardholder data",
            "Default passwords and security parameters",
            "Storing CVV/CVC codes"
          ],
          "documentation_required": [
            "Network diagrams",
            "Data flow diagrams",
            "Security policies and procedures",
            "Vulnerability scan reports",
            "Penetration testing reports",
            "Incident response procedures"
          ],
          "compliance_level": "critical",
          "penalties": "Fines up to $100,000 per month, card brand sanctions",
          "review_frequency": "annually",
          "responsible_team": "Payments and Security Team"
        }
      ]
    },
    "CCPA": {
      "description": "California Consumer Privacy Act",
      "requirements": [
        {
          "title": "Consumer Privacy Rights",
          "description": "Rights for California residents regarding their personal information",
          "applicable_scenarios": ["california residents", "personal information", "data collection", "data sales"],
          "mandatory_actions": [
            "Provide notice at collection",
            "Honor opt-out requests",
            "Enable access to personal information",
            "Allow deletion requests",
            "Provide equal service regardless of privacy choices",
            "Update privacy policy annually"
          ],
          "prohibited_actions": [
            "Selling personal info of minors under 16 without consent",
            "Discriminating against consumers exercising rights",
            "Collecting additional categories without notice"
          ],
          "documentation_required": [
            "Privacy policy",
            "Data inventory",
            "Consumer request logs",
            "Opt-out mechanisms",
            "Service provider agreements"
          ],
          "compliance_level": "critical",
          "penalties": "Up to $7,500 per intentional violation",
          "review_frequency": "annually",
          "responsible_team": "Privacy Team"
        }
      ]
    },
    "HIPAA": {
      "description": "Health Insurance Portability and Accountability Act",
      "requirements": [
        {
          "title": "Protected Health Information",
          "description": "Requirements for handling health information",
          "applicable_scenarios": ["health data", "medical records", "patient information", "health services"],
          "mandatory_actions": [
            "Implement administrative safeguards",
            "Physical security controls",
            "Technical safeguards for ePHI",
            "Business Associate Agreements",
            "Workforce training",
            "Risk assessments"
          ],
          "prohibited_actions": [
            "Unauthorized disclosure of PHI",
            "Accessing PHI without authorization",
            "Failing to provide patient access",
            "Not reporting breaches"
          ],
          "documentation_required": [
            "Risk assessments",
            "Security policies",
            "Training records",
            "BAA agreements",
            "Incident reports",
            "Access logs"
          ],
          "compliance_level": "critical",
          "penalties": "Up to $50,000 per violation, criminal charges possible",
          "review_frequency": "annually",
          "responsible_team": "Healthcare Compliance Team"
        }
      ]
    }
  },
  "general_guidance": [
    "Always consult legal team before processing personal data",
    "Document all compliance-related decisions and implementations",
    "Regular training on compliance requirements for all employees",
    "Implement privacy by design in all new systems",
    "Maintain incident response procedures for compliance violations",
    "Conduct regular compliance audits and assessments",
    "Keep up to date with changing regulations",
    "When in doubt, choose the most restrictive interpretation"
  ]
}'::jsonb);

-- 5. TROUBLESHOOTING DATA
-- ============================================================================

-- Common Errors
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('troubleshooting', 'errors', 'common_errors.json', 'support_info', '{
  "error_patterns": {
    "connection_errors": {
      "type": "Connection Error",
      "description": "Issues connecting to databases or external services",
      "patterns": [
        "connection refused",
        "connection timeout",
        "connection reset",
        "cannot connect to",
        "connection failed",
        "ECONNREFUSED",
        "ETIMEDOUT"
      ],
      "common_causes": [
        "Service not running or accessible",
        "Network connectivity issues",
        "Incorrect connection configuration",
        "Firewall blocking connection",
        "Service overloaded or down",
        "DNS resolution failures"
      ],
      "initial_steps": [
        "Check if the service is running",
        "Verify network connectivity",
        "Check connection configuration",
        "Review firewall settings",
        "Check service logs for errors",
        "Test DNS resolution"
      ],
      "severity": "high"
    },
    "authentication_errors": {
      "type": "Authentication Error",
      "description": "Problems with user authentication and authorization",
      "patterns": [
        "unauthorized",
        "authentication failed",
        "invalid token",
        "token expired",
        "access denied",
        "forbidden",
        "401",
        "403"
      ],
      "common_causes": [
        "Expired or invalid JWT token",
        "Incorrect credentials",
        "Missing authentication headers",
        "Insufficient permissions",
        "Auth service unavailable",
        "Token not refreshed"
      ],
      "initial_steps": [
        "Check token expiration and validity",
        "Verify authentication headers",
        "Confirm user permissions",
        "Check auth service status",
        "Review authentication flow",
        "Try refreshing the token"
      ],
      "severity": "medium"
    },
    "import_errors": {
      "type": "Import/Module Error",
      "description": "Issues with importing modules or packages",
      "patterns": [
        "modulenotfounderror",
        "importerror",
        "no module named",
        "cannot import",
        "module not found",
        "failed to import"
      ],
      "common_causes": [
        "Missing dependency installation",
        "Incorrect virtual environment",
        "Python path issues",
        "Typo in import statement",
        "Package not installed",
        "Version mismatch"
      ],
      "initial_steps": [
        "Check if package is installed",
        "Verify virtual environment is activated",
        "Check Python path configuration",
        "Review import statement syntax",
        "Install missing dependencies",
        "Check package version compatibility"
      ],
      "severity": "medium"
    },
    "database_errors": {
      "type": "Database Error",
      "description": "Database connection and query issues",
      "patterns": [
        "database connection",
        "sql error",
        "table doesn''t exist",
        "column not found",
        "database locked",
        "duplicate key",
        "constraint violation"
      ],
      "common_causes": [
        "Database server not running",
        "Incorrect database credentials",
        "Missing database migrations",
        "Network connectivity to database",
        "Database schema out of sync",
        "Transaction deadlock"
      ],
      "initial_steps": [
        "Check database server status",
        "Verify database credentials",
        "Run pending migrations",
        "Check database connectivity",
        "Review database schema",
        "Check for long-running queries"
      ],
      "severity": "high"
    },
    "memory_errors": {
      "type": "Memory Error",
      "description": "Out of memory or memory leak issues",
      "patterns": [
        "out of memory",
        "memory error",
        "heap space",
        "cannot allocate",
        "memory leak",
        "oom"
      ],
      "common_causes": [
        "Insufficient system memory",
        "Memory leaks in code",
        "Large data processing",
        "Infinite loops",
        "Circular references",
        "Cache overflow"
      ],
      "initial_steps": [
        "Check system memory usage",
        "Review code for memory leaks",
        "Implement pagination for large datasets",
        "Check for infinite loops",
        "Monitor memory profiling",
        "Increase heap size if needed"
      ],
      "severity": "critical"
    }
  }
}'::jsonb);

-- Diagnostics
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('troubleshooting', 'diagnostics', 'diagnostics.json', 'support_info', '{
  "components": {
    "system": {
      "basic": {
        "checks": [
          {
            "name": "CPU Usage",
            "description": "Check current CPU utilization",
            "expected": "< 80%",
            "mock_status": "pass",
            "mock_value": "45%",
            "mock_message": "CPU usage is within normal range"
          },
          {
            "name": "Memory Usage",
            "description": "Check available system memory",
            "expected": "< 85%",
            "mock_status": "pass",
            "mock_value": "67%",
            "mock_message": "Memory usage is acceptable"
          },
          {
            "name": "Disk Space",
            "description": "Check available disk space",
            "expected": "> 10GB free",
            "mock_status": "warning",
            "mock_value": "8.2GB free",
            "mock_message": "Disk space running low",
            "severity": "medium",
            "suggested_action": "Clean up temporary files or expand storage"
          },
          {
            "name": "System Load",
            "description": "Check system load average",
            "expected": "< 4.0",
            "mock_status": "pass",
            "mock_value": "2.3",
            "mock_message": "System load is normal"
          }
        ],
        "recommendations": [
          "Monitor system resources regularly",
          "Set up alerts for resource thresholds",
          "Consider system cleanup if disk space low",
          "Review resource-intensive processes"
        ]
      },
      "detailed": {
        "checks": [
          {
            "name": "Process Count",
            "description": "Number of running processes",
            "expected": "< 500",
            "mock_status": "pass",
            "mock_value": "287",
            "mock_message": "Process count is normal"
          },
          {
            "name": "Open File Descriptors",
            "description": "Check open file descriptor count",
            "expected": "< 80% of limit",
            "mock_status": "pass",
            "mock_value": "45% of limit",
            "mock_message": "File descriptor usage is healthy"
          },
          {
            "name": "Network Connections",
            "description": "Active network connections",
            "expected": "< 10000",
            "mock_status": "pass",
            "mock_value": "3421",
            "mock_message": "Network connection count is normal"
          }
        ],
        "recommendations": [
          "Monitor process lifecycle",
          "Check for zombie processes",
          "Review network connection patterns"
        ]
      }
    },
    "database": {
      "basic": {
        "checks": [
          {
            "name": "Database Connection",
            "description": "Test connection to primary database",
            "expected": "Connected",
            "mock_status": "pass",
            "mock_value": "Connected",
            "mock_message": "Database connection successful"
          },
          {
            "name": "Connection Pool",
            "description": "Check database connection pool health",
            "expected": "< 80% utilized",
            "mock_status": "pass",
            "mock_value": "45% utilized",
            "mock_message": "Connection pool healthy"
          },
          {
            "name": "Query Performance",
            "description": "Check average query response time",
            "expected": "< 100ms",
            "mock_status": "pass",
            "mock_value": "23ms average",
            "mock_message": "Query performance good"
          }
        ],
        "recommendations": [
          "Monitor database performance metrics",
          "Optimize slow queries",
          "Consider read replicas for high load"
        ]
      },
      "performance": {
        "checks": [
          {
            "name": "Slow Query Count",
            "description": "Number of slow queries in last hour",
            "expected": "< 10",
            "mock_status": "warning",
            "mock_value": "15",
            "mock_message": "Elevated slow query count",
            "severity": "medium",
            "suggested_action": "Review and optimize slow queries"
          },
          {
            "name": "Lock Wait Time",
            "description": "Average lock wait time",
            "expected": "< 50ms",
            "mock_status": "pass",
            "mock_value": "12ms",
            "mock_message": "Lock contention is minimal"
          },
          {
            "name": "Cache Hit Rate",
            "description": "Database cache hit rate",
            "expected": "> 90%",
            "mock_status": "pass",
            "mock_value": "94%",
            "mock_message": "Cache performance is excellent"
          }
        ],
        "recommendations": [
          "Analyze slow query log",
          "Consider query optimization",
          "Review indexing strategy"
        ]
      }
    },
    "network": {
      "basic": {
        "checks": [
          {
            "name": "Internet Connectivity",
            "description": "Test external network connectivity",
            "expected": "Connected",
            "mock_status": "pass",
            "mock_value": "Connected",
            "mock_message": "Internet connectivity working"
          },
          {
            "name": "DNS Resolution",
            "description": "Test DNS name resolution",
            "expected": "Working",
            "mock_status": "pass",
            "mock_value": "Working",
            "mock_message": "DNS resolution successful"
          },
          {
            "name": "Internal Network",
            "description": "Test internal network connectivity",
            "expected": "Connected",
            "mock_status": "pass",
            "mock_value": "Connected",
            "mock_message": "Internal network operational"
          }
        ],
        "recommendations": [
          "Monitor network latency",
          "Set up backup DNS servers",
          "Configure network redundancy"
        ]
      }
    },
    "services": {
      "basic": {
        "checks": [
          {
            "name": "Authentication Service",
            "description": "Check auth service health",
            "expected": "Running",
            "mock_status": "pass",
            "mock_value": "Running",
            "mock_message": "Authentication service healthy"
          },
          {
            "name": "Payment Gateway",
            "description": "Check payment service status",
            "expected": "Running",
            "mock_status": "fail",
            "mock_value": "Error",
            "mock_message": "Payment service responding slowly",
            "severity": "high",
            "suggested_action": "Check payment service logs and restart if needed"
          },
          {
            "name": "Notification Service",
            "description": "Check notification service",
            "expected": "Running",
            "mock_status": "pass",
            "mock_value": "Running",
            "mock_message": "Notification service operational"
          },
          {
            "name": "Cache Service",
            "description": "Check Redis cache status",
            "expected": "Running",
            "mock_status": "pass",
            "mock_value": "Running",
            "mock_message": "Cache service healthy"
          }
        ],
        "recommendations": [
          "Implement service health monitoring",
          "Set up automatic service restart",
          "Monitor service dependencies"
        ]
      }
    }
  }
}'::jsonb);

-- Solutions
INSERT INTO json_documents (category, subcategory, filename, document_type, data) VALUES 
('troubleshooting', 'solutions', 'solutions.json', 'support_info', '{
  "solutions": [
    {
      "title": "Fix Database Connection Refused Error",
      "category": "database",
      "description": "Resolve connection refused errors when connecting to PostgreSQL database",
      "difficulty": "beginner",
      "estimated_time": "10 minutes",
      "keywords": ["database", "connection", "refused", "postgresql", "postgres"],
      "prerequisites": ["Database credentials", "Network access", "Terminal access"],
      "steps": [
        "Check if PostgreSQL service is running: `sudo systemctl status postgresql`",
        "Verify database credentials in your .env file",
        "Test database connectivity: `psql -h localhost -U username -d database_name`",
        "Check firewall settings allow connections on port 5432",
        "Restart PostgreSQL service if needed: `sudo systemctl restart postgresql`",
        "Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql.log`"
      ],
      "verification": [
        "Connection test succeeds without errors",
        "Application can query database successfully",
        "No connection errors in application logs"
      ],
      "prevention": [
        "Monitor database service health",
        "Set up database connection pooling",
        "Configure proper timeout settings",
        "Implement retry logic with exponential backoff"
      ],
      "related_issues": ["timeout errors", "authentication failed", "network unreachable"]
    },
    {
      "title": "Resolve JWT Token Expired Errors",
      "category": "authentication",
      "description": "Handle expired JWT tokens and implement proper token refresh",
      "difficulty": "intermediate",
      "estimated_time": "15 minutes",
      "keywords": ["jwt", "token", "expired", "authentication", "refresh"],
      "prerequisites": ["Valid refresh token", "Auth service access"],
      "steps": [
        "Check token expiration time in JWT payload",
        "Implement automatic token refresh logic",
        "Use refresh token to get new access token",
        "Update Authorization header with new token",
        "Handle refresh token rotation if implemented",
        "Implement token refresh 5 minutes before expiration"
      ],
      "verification": [
        "API calls succeed with refreshed token",
        "No more authentication errors",
        "Token refresh happens automatically"
      ],
      "prevention": [
        "Implement proactive token refresh",
        "Set appropriate token expiration times",
        "Handle token refresh errors gracefully",
        "Store refresh token securely"
      ],
      "related_issues": ["unauthorized access", "authentication failed", "invalid token"]
    },
    {
      "title": "Fix ModuleNotFoundError for Python Packages",
      "category": "environment",
      "description": "Resolve missing Python module errors and dependency issues",
      "difficulty": "beginner",
      "estimated_time": "5 minutes",
      "keywords": ["python", "module", "import", "package", "dependencies", "pip"],
      "prerequisites": ["Python virtual environment", "Requirements file"],
      "steps": [
        "Activate your virtual environment: `source .venv/bin/activate`",
        "Check if package is installed: `pip list | grep package_name`",
        "Install missing package: `pip install package_name`",
        "Or install from requirements: `pip install -r requirements.txt`",
        "Verify import works: `python -c ''import package_name''`",
        "Clear Python cache if needed: `find . -type d -name __pycache__ -exec rm -r {} +`"
      ],
      "verification": [
        "Import statement works without errors",
        "Package appears in pip list output",
        "Application starts successfully"
      ],
      "prevention": [
        "Always use virtual environments",
        "Keep requirements.txt updated",
        "Document all dependencies clearly",
        "Use pip freeze to capture exact versions"
      ],
      "related_issues": ["import errors", "dependency conflicts", "version mismatch"]
    },
    {
      "title": "Debug API Endpoint Not Found (404) Errors",
      "category": "api",
      "description": "Troubleshoot HTTP 404 errors when calling API endpoints",
      "difficulty": "intermediate",
      "estimated_time": "20 minutes",
      "keywords": ["api", "404", "endpoint", "not found", "routing"],
      "prerequisites": ["API documentation", "Request details", "API testing tool"],
      "steps": [
        "Verify the correct API base URL and endpoint path",
        "Check if the HTTP method (GET/POST/PUT/DELETE) is correct",
        "Review API documentation for exact endpoint specification",
        "Test with API client like Postman or curl",
        "Check server logs for routing errors",
        "Verify API version in URL path if versioned",
        "Check for trailing slashes in URL"
      ],
      "verification": [
        "API endpoint returns expected response",
        "No 404 errors in server logs",
        "Request reaches the correct handler"
      ],
      "prevention": [
        "Use API documentation consistently",
        "Implement proper API versioning",
        "Add endpoint testing to CI/CD",
        "Use API client generation tools"
      ],
      "related_issues": ["routing errors", "api versioning", "method not allowed"]
    },
    {
      "title": "Resolve Docker Container Connection Issues",
      "category": "infrastructure",
      "description": "Fix networking issues between Docker containers",
      "difficulty": "advanced",
      "estimated_time": "25 minutes",
      "keywords": ["docker", "container", "network", "connection", "compose"],
      "prerequisites": ["Docker installed", "Docker Compose file", "Container logs access"],
      "steps": [
        "Check if containers are running: `docker ps`",
        "Verify containers are on same network: `docker network ls`",
        "Use container name instead of localhost",
        "Check Docker Compose network configuration",
        "Test connectivity: `docker exec container1 ping container2`",
        "Review exposed ports in Dockerfile",
        "Check environment variables for service URLs"
      ],
      "verification": [
        "Containers can communicate",
        "Services respond to requests",
        "No connection refused errors"
      ],
      "prevention": [
        "Use Docker Compose for multi-container apps",
        "Define explicit networks",
        "Use service discovery",
        "Document container dependencies"
      ],
      "related_issues": ["port binding", "network isolation", "dns resolution"]
    }
  ]
}');

-- ============================================================================
-- VERIFICATION AND SUMMARY
-- ============================================================================

-- Check total records inserted
SELECT 
    category,
    subcategory,
    COUNT(*) as total_documents
FROM json_documents 
GROUP BY category, subcategory
ORDER BY category, subcategory;

-- Summary of all data
SELECT 
    'Total Documents Loaded' as summary,
    COUNT(*) as count
FROM json_documents;

-- Sample queries to test the data
-- Find all team members with Python expertise
SELECT 
    category,
    filename,
    jsonb_array_elements(data->'members')->>'name' as member_name,
    jsonb_array_elements(data->'members')->>'role' as role
FROM json_documents 
WHERE category = 'teams' 
    AND filename = 'team_members.json'
    AND data->'members' @> '[{"expertise": ["Python"]}]';

-- Search for authentication-related information
SELECT 
    category,
    subcategory,
    filename,
    data->>'name' as name,
    data->>'description' as description
FROM json_documents 
WHERE data::text ILIKE '%authentication%'
   OR data::text ILIKE '%auth%'
   OR data::text ILIKE '%jwt%';

-- Find all Python repositories
SELECT 
    data->'repositories' as repositories
FROM json_documents 
WHERE category = 'codebase' 
    AND filename = 'repositories.json'
    AND data->'repositories' @> '[{"language": "Python"}]';











-- Create a single tickets table including reporter names and emails from onboard.sql
CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(50) DEFAULT 'medium',
    reporter_name VARCHAR(100),
    reporter_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Function to update the updated_at timestamp automatically
CREATE OR REPLACE FUNCTION update_ticket_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to execute the timestamp update function
CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_ticket_updated_at();

-- Insert sample tickets using all names and emails from onboard.sql team_members.json
INSERT INTO tickets (title, description, status, priority, reporter_name, reporter_email) VALUES
('Login Failure on Edge Browser', 'Users report login issues specific to Edge', 'open', 'high', 'Alice Chen', 'alice.chen@company.com'),
('API Rate Limit Exceeded', 'Payment API hitting rate limits', 'open', 'medium', 'Bob Johnson', 'bob.johnson@company.com'),
('UI Glitch in Dashboard', 'Dashboard widgets misaligned', 'in progress', 'low', 'Carol White', 'carol.white@company.com'),
('Payment Timeout Error', 'Intermittent payment processing delays', 'open', 'high', 'Eric Wang', 'eric.wang@company.com'),
('Fraud Detection False Positive', 'Legitimate transactions flagged', 'open', 'medium', 'Grace Kim', 'grace.kim@company.com'),
('Slow Page Load Times', 'Frontend performance degradation', 'in progress', 'medium', 'Henry Taylor', 'henry.taylor@company.com'),
('Accessibility Issue in Forms', 'Screen reader compatibility problem', 'open', 'high', 'Isabel Martinez', 'isabel.martinez@company.com'),
('Deployment Pipeline Failure', 'CI/CD pipeline stalling', 'open', 'high', 'Laura Anderson', 'laura.anderson@company.com'),
('Service Downtime Alert', 'Authentication service outage', 'resolved', 'critical', 'Mark Thompson', 'mark.thompson@company.com'),
('Data Pipeline Latency', 'Analytics data delayed', 'open', 'medium', 'Olivia Parker', 'olivia.parker@company.com'),
('ML Model Prediction Error', 'Incorrect fraud predictions', 'in progress', 'high', 'Peter Zhang', 'peter.zhang@company.com'),
('Session Timeout Bug', 'Users logged out unexpectedly', 'open', 'medium', 'Mike Rodriguez', 'mike.rodriguez@company.com'),
('Payment Gateway Sync Issue', 'Transactions not syncing', 'open', 'high', 'Jennifer Liu', 'jennifer.liu@company.com');



COMMIT;

