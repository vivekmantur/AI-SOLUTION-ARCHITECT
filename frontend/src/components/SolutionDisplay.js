import React, { useEffect, useRef, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Divider,
  Alert,
  Chip,
  Card,
  CardContent,
  Button,
  Collapse,
  IconButton,
} from '@mui/material';
import mermaid from 'mermaid';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArchitectureIcon from '@mui/icons-material/Architecture';
import AccountTreeIcon from '@mui/icons-material/AccountTree';
import ExtensionIcon from '@mui/icons-material/Extension';
import SecurityIcon from '@mui/icons-material/Security';
import BuildIcon from '@mui/icons-material/Build';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import ApiIcon from '@mui/icons-material/Api';
import CodeIcon from '@mui/icons-material/Code';
import NotesIcon from '@mui/icons-material/Notes';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';


const AZURE_ICON_BASE = "/azure-icons";

const normalize = (s) =>
  s
    ?.toLowerCase()
    .replace(/^azure\s+/i, "")   // remove leading "Azure "
    .replace(/\s+sql$/, " sql")  // normalize SQL suffix
    .replace(/^aws\s+/i, "")
    .replace(/^gcp\s+/i, "")
    .replace(/\(.*?\)/g, "")
    .trim();

const resolveAzureIcon = (cloudService) => {
  if (!cloudService) return null;

  const map = {
  /* =======================
     ANALYTICS
  ======================= */
  "application insights": "analytics/Application_Insights.svg",
  "data factory": "analytics/Data_Factory.svg",
  "databricks": "analytics/Databricks.svg",
  "machine learning": "analytics/Machine_Learning.svg",
  "monitor": "analytics/Monitor.svg",
  "power bi": "analytics/Power_BI.svg",
  "synapse analytics": "analytics/Synapse_Analytics.svg",
  "synapse sql": "analytics/Synapse_Analytics.svg",

  /* =======================
     COMPUTE
  ======================= */
  "app service": "compute/App_Service.svg",
  "container apps": "compute/Container_Apps.svg",
  "function app": "compute/Function_Apps.svg",
  "functions": "compute/Function_Apps.svg",
  "kubernetes service": "compute/Kubernetes_Services.svg",
  "aks": "compute/Kubernetes_Services.svg",
  "static web apps": "compute/Static_Web_Apps.svg",

  /* =======================
     DATABASES / STORAGE
  ======================= */
  "cache for redis": "databases/Cache_For_Redis.svg",
  "redis cache": "databases/Cache_For_Redis.svg",
  "cosmos db": "databases/Cosmos_DB.svg",
  "data lake": "databases/Data_Lake_Storage.svg",
  "data lake storage": "databases/Data_Lake_Storage.svg",
  "data lake storage gen2": "databases/Data_Lake_Storage.svg",
  "sql database": "databases/SQL_Database.svg",
  "azure sql": "databases/SQL_Database.svg",
  "storage account": "databases/Storage_Accounts.svg",
  "blob storage": "databases/Storage_Accounts.svg",

  /* =======================
     INTEGRATION
  ======================= */
  "api gateway": "integration/API_Management.svg",
  "event grid": "integration/Event_Grid.svg",
  "event hubs": "integration/Event_Hubs.svg",
  "logic apps": "integration/Logic_Apps.svg",
  "notification hubs": "integration/Notification_Hubs.svg",
  "service bus": "integration/Service_Bus.svg",

  /* =======================
     NETWORKING
  ======================= */
  "application gateway": "networking/Application_Gateways.svg",
  "front door": "networking/Front_Door.svg",
  "load balancer": "networking/Load_Balancers.svg",
  "virtual network": "networking/Virtual_Networks.svg",
  "vnet": "networking/Virtual_Networks.svg",

  /* =======================
     SECURITY
  ======================= */
  "azure active directory": "security/Azure_Active_Directory.svg",
  "azure ad": "security/Azure_Active_Directory.svg",
  "ddos protection": "security/DDoS_Protection.svg",
  "firewall": "security/Firewall.svg",
  "key vault": "security/Key_Vaults.svg",
};



  const key = normalize(cloudService);
  const icon = map[key];

  if (!icon) {
    console.warn("❌ No icon mapping for:", cloudService);
    return null;
  }

  return `${AZURE_ICON_BASE}/${icon}`;
};


const AWS_ICON_BASE = "/aws-icons";

const resolveAwsIcon = (cloudService) => {
  if (!cloudService) return null;

  const map = {
    // analytics
    "athena": "analytics/Athena.svg",
    "glue": "analytics/Glue.svg",
    "kinesis": "analytics/Kinesis.svg",
    "quicksight": "analytics/QuickSight.svg",
    "redshift": "analytics/Redshift.svg",
    "emr": "analytics/EMR.svg",

    // compute
    "ec2": "compute/EC2.svg",
    "lambda": "compute/Lambda.svg",
    "ecs": "compute/ECS.svg",
    "eks": "compute/EKS.svg",
    "fargate": "compute/Fargate.svg",
    "elastic beanstalk": "compute/Elastic_Beanstalk.svg",

    // databases
    "rds": "databases/RDS.svg",
    "dynamodb": "databases/DynamoDB.svg",
    "aurora": "databases/Aurora.svg",
    "elasticache": "databases/ElastiCache.svg",
    "neptune": "databases/Neptune.svg",

    // integration
    "sqs": "integration/SQS.svg",
    "sns": "integration/SNS.svg",
    "eventbridge": "integration/EventBridge.svg",
    "step functions": "integration/StepFunctions.svg",
    "api gateway": "integration/API_Gateway.svg",

    // networking
    "vpc": "networking/VPC.svg",
    "route 53": "networking/Route53.svg",
    "cloudfront": "networking/CloudFront.svg",
    "elastic load balancer": "networking/Elastic_Load_Balancer.svg",
    "nat gateway": "networking/NAT_Gateway.svg",

    // security
    "iam": "security/IAM.svg",
    "cognito": "security/Cognito.svg",
    "kms": "security/KMS.svg",
    "waf": "security/WAF.svg",
    "shield": "security/Shield.svg",
    "secrets manager": "security/Secrets_Manager.svg",

    // storage
    "s3": "storage/S3.svg",
    "ebs": "storage/EBS.svg",
    "efs": "storage/EFS.svg",
    "glacier": "storage/Glacier.svg",
  };

  const key = normalize(cloudService);
  const icon = map[key];

  if (!icon) {
    console.warn("❌ No AWS icon mapping for:", cloudService);
    return null;
  }

  return `${AWS_ICON_BASE}/${icon}`;
};

const GCP_ICON_BASE = "/gcp-icons";

const resolveGcpIcon = (cloudService) => {
  if (!cloudService) return null;

  const map = {
    // analytics
    "bigquery": "analytics/BigQuery.svg",
    "dataflow": "analytics/Dataflow.svg",
    "dataproc": "analytics/Dataproc.svg",
    "pubsub": "analytics/PubSub.svg",
    "pub sub": "analytics/PubSub.svg",
    "looker": "analytics/Looker.svg",

    // compute
    "compute engine": "compute/Compute_Engine.svg",
    "app engine": "compute/App_Engine.svg",
    "cloud functions": "compute/Cloud_Functions.svg",
    "cloud run": "compute/Cloud_Run.svg",
    "gke": "compute/GKE.svg",
    "google kubernetes engine": "compute/GKE.svg",

    // databases
    "cloud sql": "databases/Cloud_SQL.svg",
    "firestore": "databases/Firestore.svg",
    "bigtable": "databases/Bigtable.svg",
    "spanner": "databases/Spanner.svg",
    "memorystore": "databases/Memorystore.svg",

    // integration
    "cloud tasks": "integration/Cloud_Tasks.svg",
    "workflows": "integration/Workflows.svg",
    "api gateway": "integration/API_Gateway.svg",
    "pubsub integration": "integration/PubSub.svg",

    // networking
    "vpc": "networking/VPC.svg",
    "cloud load balancing": "networking/Cloud_Load_Balancing.svg",
    "cloud cdn": "networking/Cloud_CDN.svg",
    "cloud dns": "networking/Cloud_DNS.svg",
    "cloud nat": "networking/Cloud_NAT.svg",

    // security
    "iam": "security/IAM.svg",
    "cloud kms": "security/Cloud_KMS.svg",
    "secret manager": "security/Secret_Manager.svg",
    "cloud armor": "security/Cloud_Armor.svg",
    "security command center": "security/Security_Command_Center.svg",

    // storage
    "cloud storage": "storage/Cloud_Storage.svg",
    "filestore": "storage/Filestore.svg",
    "persistent disk": "storage/Persistent_Disk.svg",
    "archive storage": "storage/Archive_Storage.svg",

    // ai-ml
    "vertex ai": "ai-ml/Vertex_AI.svg",
    "automl": "ai-ml/AutoML.svg",
    "vision ai": "ai-ml/Vision_AI.svg",
    "natural language ai": "ai-ml/Natural_Language_AI.svg",

    // devops
    "cloud build": "devops/Cloud_Build.svg",
    "artifact registry": "devops/Artifact_Registry.svg",
    "cloud deploy": "devops/Cloud_Deploy.svg",
    "cloud monitoring": "devops/Cloud_Monitoring.svg",
    "cloud logging": "devops/Cloud_Logging.svg",
  };

  const key = normalize(cloudService);
  const icon = map[key];

  if (!icon) {
    console.warn("❌ No GCP icon mapping for:", cloudService);
    return null;
  }

  return `${GCP_ICON_BASE}/${icon}`;
};

const resolveCloudIcon = (cloudService) => {
  if (!cloudService) return null;

  const s = cloudService.toLowerCase();

  // Azure detection
  if (s.includes("azure") || s.includes("synapse") || s.includes("cosmos") || s.includes("power bi")) {
    return resolveAzureIcon(cloudService);
  }

  // AWS detection
  if (s.includes("aws") || s.includes("ec2") || s.includes("s3") || s.includes("lambda") || s.includes("dynamodb")) {
    return resolveAwsIcon(cloudService);
  }

  // GCP detection
  if (s.includes("gcp") || s.includes("bigquery") || s.includes("cloud run") || s.includes("gke") || s.includes("firestore")) {
    return resolveGcpIcon(cloudService);
  }

  // fallback try all
  return (
    resolveAzureIcon(cloudService) ||
    resolveAwsIcon(cloudService) ||
    resolveGcpIcon(cloudService)
  );
};


// 🔧 Convert component name to Mermaid-safe node ID
const toNodeId = (name) =>
  name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_|_$/g, "");


const SECTIONS = {
  REQUIREMENTS: 'requirements',
  ARCHITECTURE: 'architecture',
  DIAGRAM: 'diagram',
  CLOUD_DIAGRAM: 'cloud_diagram',
  COMPONENTS: 'components',
  NFR: 'nfr',
  TECH: 'tech',
  COST: 'cost',
  API: 'api',
  IAC: 'iac',
  NOTES: 'notes',
};


const SolutionDisplay = ({ solution }) => {
  const mermaidRef = useRef(null);
   const diagramRef = useRef(null);
  const cloudDiagramRef = useRef(null);
  const [showRawDiagram, setShowRawDiagram] = useState(false);
  const [diagramError, setDiagramError] = useState(null);
  const [copySuccess, setCopySuccess] = useState(false);
  const [activeSection, setActiveSection] = useState(SECTIONS.REQUIREMENTS);


  useEffect(() => {
    // Initialize mermaid once
    mermaid.initialize({ 
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#3b82f6',
        primaryTextColor: '#000000',
        primaryBorderColor: '#2563eb',
        lineColor: '#374151',
        secondaryColor: '#8b5cf6',
        secondaryTextColor: '#000000',
        tertiaryColor: '#f3f4f6',
        tertiaryTextColor: '#000000',
        background: '#ffffff',
        mainBkg: '#ffffff',
        textColor: '#000000',
        labelTextColor: '#000000',
        nodeBorder: '#2563eb',
        nodeTextColor: '#000000',
        clusterBkg: '#e0e7ff',
        clusterBorder: '#3b82f6',
        edgeLabelBackground: '#ffffff',
        fontSize: '14px',
        fontFamily: 'Arial, sans-serif',
      },
      securityLevel: 'loose',
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
        nodeSpacing: 80,
        rankSpacing: 80,
        useMaxWidth: false,
      },
    });
  }, []);




const enrichMermaidWithIcons = (mermaidCode, components) => {
  let enriched = mermaidCode;

  for (const c of components) {
    const iconPath = resolveCloudIcon(c.cloud_service);

    if (!iconPath) continue;

    const safeLabel = c.name.replace(/"/g, '\\"');

    const htmlLabel = `
<div style="display:flex;flex-direction:column;align-items:center;gap:6px">
  <div>${safeLabel}</div>
  <img src="${iconPath}" width="32" height="32"/>
</div>
`.trim();

    // replace only the label text
    const regex = new RegExp(
      `\\["${safeLabel}"\\]`,
      "g"
    );

    enriched = enriched.replace(
      regex,
      `["${htmlLabel}"]`
    );
  }

  return enriched;
};



 useEffect(() => {
  const renderDiagram = async () => {
    const targetRef =
      activeSection === SECTIONS.CLOUD_DIAGRAM
        ? cloudDiagramRef
        : diagramRef;

    if (!solution?.mermaid_diagram || !targetRef.current) return;

    try {
      targetRef.current.innerHTML = '';
      setDiagramError(null);

      const renderId = `architecture-${activeSection}-${Date.now()}`;
      const diagramSource =
        activeSection === SECTIONS.CLOUD_DIAGRAM
          ? enrichMermaidWithIcons(
              solution.mermaid_diagram,
              solution.components || []
            )
          : solution.mermaid_diagram;

      const { svg } = await mermaid.render(renderId, diagramSource);

      targetRef.current.innerHTML = svg;


      // 2️⃣ ONLY AFTER SVG EXISTS → inject icons
      if (activeSection === SECTIONS.CLOUD_DIAGRAM) {
        const renderedSvg = targetRef.current.querySelector("svg");
        console.log("SVG AFTER RENDER?", !!renderedSvg);

       

      }

    } catch (error) {
      console.error("Mermaid render error:", error);
      setDiagramError(error.message);
      targetRef.current.innerHTML = '';
    }
  };

  renderDiagram();
}, [solution, activeSection]);






  const handleCopyDiagram = () => {
    if (solution?.mermaid_diagram) {
      navigator.clipboard.writeText(solution.mermaid_diagram);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };



  return (
    <Box>
      <Alert 
        icon={<CheckCircleIcon fontSize="inherit" />} 
        severity="success"
        
        sx={{ mb: 3 }}
      >
        Solution Design Successfully Generated
      </Alert>
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {Object.values(SECTIONS).map((section) => (
            <Button
              key={section}
              size="small"
              variant={activeSection === section ? 'contained' : 'outlined'}
              onClick={() => setActiveSection(section)}
            >
              {section.toUpperCase()}
            </Button>
          ))}
        </Box>
      </Paper>

      {/* Normalized Requirements */}
      {
      activeSection === SECTIONS.REQUIREMENTS && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <AccountTreeIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             2️⃣ Normalized Understanding of Requirements
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {JSON.stringify(solution.normalized_requirements, null, 2)}
        </Box>
      </Paper>
      )}

      <Divider sx={{ my: 3 }} />

      {/* Architecture Description */}
      {
        activeSection === SECTIONS.ARCHITECTURE && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ArchitectureIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             3️⃣ Architecture Overview
          </Typography>
        </Box>
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {solution.architecture_description || 'No description provided.'}
        </Typography>
      </Paper>
      )}
      {/* Mermaid Diagram */}
      {
      activeSection === SECTIONS.DIAGRAM && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AccountTreeIcon sx={{ mr: 1 }} />
            <Typography variant="h6">
               4️⃣ Architecture Diagram (Visual)
            </Typography>
          </Box>
          {solution.mermaid_diagram && (
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                size="small"
                startIcon={<ContentCopyIcon />}
                onClick={handleCopyDiagram}
                variant="outlined"
              >
                {copySuccess ? 'Copied!' : 'Copy Code'}
              </Button>
              <Button
                size="small"
                endIcon={<ExpandMoreIcon sx={{ transform: showRawDiagram ? 'rotate(180deg)' : 'rotate(0deg)', transition: '0.3s' }} />}
                onClick={() => setShowRawDiagram(!showRawDiagram)}
                variant="outlined"
              >
                {showRawDiagram ? 'Hide' : 'Show'} Raw Code
              </Button>
            </Box>
          )}
        </Box>
        
        {solution.mermaid_diagram ? (
          <>
            {diagramError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Error rendering diagram:</strong>
                </Typography>
                <Typography variant="body2" sx={{ fontFamily: 'monospace', mb: 1 }}>
                  {diagramError}
                </Typography>
                <Typography variant="body2">
                  The diagram code has been sanitized but may still contain syntax errors. 
                  Please check the raw code below or try regenerating the design.
                </Typography>
              </Alert>
            )}
            
            <Collapse in={showRawDiagram}>
              <Box 
                component="pre" 
                sx={{ 
                  backgroundColor: '#1e1e1e', 
                  color: '#d4d4d4',
                  p: 2, 
                  borderRadius: 1,
                  overflow: 'auto',
                  fontSize: '0.875rem',
                  mb: 2,
                  maxHeight: '300px',
                }}
              >
                
                {solution.mermaid_diagram}
              </Box>
            </Collapse>
            
            <Box 
              ref={diagramRef}
              sx={{ 
                display: 'flex', 
                justifyContent: 'center',
                p: 2,
                backgroundColor: '#ffffff',
                borderRadius: 1,
                overflow: 'auto',
                minHeight: diagramError ? '100px' : '200px',
                '& svg': {
                  maxWidth: '100%',
                  height: 'auto',
                },
                '& .node text, & .edgeLabel text, & text': {
                  fill: '#000000 !important',
                  fontWeight: '500 !important',
                  fontSize: '14px !important',
                },
                '& .label': {
                  color: '#000000 !important',
                },
              }}
            />
          </>
        ) : (
          <Alert severity="warning">No diagram available</Alert>
        )}
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />

      {/* Components */}
      {activeSection === SECTIONS.COMPONENTS && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ExtensionIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             5️⃣ Key Components and Cloud Services
          </Typography>
        </Box>
        {solution.components?.map((component, index) => (
          <Card key={index} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔹 {component.name} <Chip label={component.type} size="small" sx={{ ml: 1 }} />
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                ☁️ Service: <strong>{component.cloud_service || 'N/A'}</strong>
              </Typography>
              <Typography variant="body2">
                📄 {component.description || 'No description'}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Paper>
      )}

      {/* Non-Functional Requirements */}
      {activeSection === SECTIONS.NFR && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SecurityIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             6️⃣ Non-Functional Requirements
          </Typography>
        </Box>
        {solution.non_functional_considerations?.length > 0 ? (
          <Box component="ul" sx={{ pl: 2 }}>
            {solution.non_functional_considerations.map((item, index) => (
              <Typography component="li" key={index} variant="body1" sx={{ mb: 1 }}>
                ✔️ {item}
              </Typography>
            ))}
          </Box>
        ) : (
          <Typography>No details provided.</Typography>
        )}
      </Paper>
      )}
      {/* Tech Stack */}
      {activeSection === SECTIONS.TECH && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <BuildIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             7️⃣ Proposed Tech Stack
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {solution.tech_stack?.length > 0 ? (
            solution.tech_stack.map((tech, index) => (
              <Chip key={index} label={tech} color="primary" variant="outlined" />
            ))
          ) : (
            <Typography>No tech stack generated.</Typography>
          )}
        </Box>
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />
      
      {/* Cost Estimate */}
      {activeSection === SECTIONS.COST && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <AttachMoneyIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             8️⃣ Estimated Cloud Cost Breakdown
          </Typography>
        </Box>
        <Typography variant="h5" gutterBottom color="primary">
          💵 Total Estimated Monthly Cost: ${solution.cost_estimate?.total_monthly_usd?.toFixed(2) || '0.00'}
        </Typography>
        {solution.cost_estimate?.per_environment?.map((env, index) => (
          <Typography key={index} variant="body1" sx={{ ml: 2, mb: 1 }}>
            • <strong>{env.environment}</strong> ➝ ${env.monthly_usd?.toFixed(2)}
          </Typography>
        ))}
        {solution.cost_estimate?.notes && (
          <Alert severity="info" sx={{ mt: 2 }}>
            📝 Notes: {solution.cost_estimate.notes}
          </Alert>
        )}
      </Paper>
      )}
      <Divider sx={{ my: 3 }} />

      {/* API Spec */}
      {activeSection === SECTIONS.API && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <ApiIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
             9️⃣ API Specification Stub
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {solution.api_spec_stub || 'No API stub generated.'}
        </Box>
      </Paper>
      )}
      {/* Infrastructure as Code */}
      {activeSection === SECTIONS.IAC && (
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <CodeIcon sx={{ mr: 1 }} />
          <Typography variant="h6">
            🔟 Infrastructure-as-Code Stub (Terraform/Bicep)
          </Typography>
        </Box>
        <Box 
          component="pre" 
          sx={{ 
            backgroundColor: '#1e1e1e', 
            color: '#d4d4d4',
            p: 2, 
            borderRadius: 1,
            overflow: 'auto',
            fontSize: '0.875rem',
          }}
        >
          {solution.infra_as_code_stub || 'No IaC generated.'}
        </Box>
      </Paper>
      )}

      {/* Additional Notes */}
      
      {activeSection === SECTIONS.NOTES && solution.notes && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <NotesIcon sx={{ mr: 1 }} />
            <Typography variant="h6">
              📝 Additional Notes
            </Typography>
          </Box>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {solution.notes}
          </Typography>
        </Paper>
      )}
      {activeSection === SECTIONS.CLOUD_DIAGRAM && (
  <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
      <ArchitectureIcon sx={{ mr: 1 }} />
      <Typography variant="h6">
        ☁️ Cloud Architecture Diagram
      </Typography>
    </Box>

    <Typography variant="body2" sx={{ mb: 2, color: 'text.secondary' }}>
      Logical architecture mapped to cloud services with visual icons.
    </Typography>

    <Box
  ref={cloudDiagramRef}
  sx={{
    display: 'flex',
    justifyContent: 'center',
    p: 2,
    backgroundColor: '#ffffff',
    borderRadius: 1,
    overflow: 'visible',
    '& svg': {
      overflow: 'visible',
    },
    '& .node': {
      overflow: 'visible',
    },
    '& .node > rect': {
      overflow: 'visible',
    },
  }}
/>


  </Paper>
)}

    </Box>
  );
};

export default SolutionDisplay;
