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
  TASK1: "task1",
  TASK2: "task2",
  TASK3: "task3",
  TASK4: "task4",
  TASK5: "task5",
  COMPONENTS: "components",
  DIAGRAM: "diagram",
  CLOUD_DIAGRAM: "cloud_diagram",
};

const SolutionDisplay = ({ solution }) => {
  const diagramRef = useRef(null);
  const cloudDiagramRef = useRef(null);

  const [showRawDiagram, setShowRawDiagram] = useState(false);
  const [diagramError, setDiagramError] = useState(null);
  const [copySuccess, setCopySuccess] = useState(false);

  const [activeSection, setActiveSection] = useState(SECTIONS.TASK1);

  useEffect(() => {
   mermaid.initialize({
  startOnLoad: false,
  theme: "base",
  securityLevel: "loose",
  flowchart: {
    htmlLabels: true,
    curve: "basis",
    nodeSpacing: 50,
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

      const safeLabel = (c.name || "").replace(/"/g, '\\"');

     const htmlLabel = `
      <div style="
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:4px;
        padding:2px;
        font-size:10px;
        line-height:1.1;
        text-align:center;
        width:90px;
      ">
        <div style="font-weight:600;">${safeLabel}</div>
        <img src="${iconPath}" style="width:20px;height:20px;object-fit:contain;" />
      </div>
      `.trim();



      const regex = new RegExp(`\\["${safeLabel}"\\]`, "g");
      enriched = enriched.replace(regex, `["${htmlLabel}"]`);
    }

    return enriched;
  };

useEffect(() => {
  const renderDiagram = async () => {
    const targetRef =
      activeSection === SECTIONS.CLOUD_DIAGRAM ? cloudDiagramRef : diagramRef;

    let diagramSource = solution?.task_7_mermaid_diagram || "";

    // normalize header (remove graph TD / flowchart TD)
    diagramSource = diagramSource
      .replace(/^graph\s+(TD|LR|RL|BT)\s*/i, "")
      .replace(/^flowchart\s+(TD|LR|RL|BT)\s*/i, "")
      .trim();

    if (!diagramSource || !targetRef.current) return;

    try {
      targetRef.current.innerHTML = "";
      setDiagramError(null);

      const renderId = `architecture-${activeSection}-${Date.now()}`;

      const finalDiagram =
        activeSection === SECTIONS.CLOUD_DIAGRAM
          ? `
%%{init: {"flowchart": {"nodeSpacing": 50, "rankSpacing": 80}} }%%
flowchart TD
${enrichMermaidWithIcons(diagramSource, solution?.task_6_components || [])}
`
          : solution?.task_7_mermaid_diagram || "";

      const { svg } = await mermaid.render(renderId, finalDiagram);
      targetRef.current.innerHTML = svg;
    } catch (error) {
      console.error("Mermaid render error:", error);
      setDiagramError(error.message);
      targetRef.current.innerHTML = "";
    }
  };

  renderDiagram();
}, [solution, activeSection]);


  const handleCopyDiagram = () => {
    if (solution?.task_7_mermaid_diagram) {
      navigator.clipboard.writeText(solution.task_7_mermaid_diagram);
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

      {/* Navigation */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
          <Button
            size="small"
            variant={activeSection === SECTIONS.TASK1 ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.TASK1)}
          >
            Requirements Understanding
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.TASK2 ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.TASK2)}
          >
            Architecture Overview
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.TASK3 ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.TASK3)}
          >
            Architecture Flow
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.TASK4 ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.TASK4)}
          >
            Best Architecture Recommendation
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.TASK5 ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.TASK5)}
          >
            Key Design Decisions
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.COMPONENTS ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.COMPONENTS)}
          >
            COMPONENTS
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.DIAGRAM ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.DIAGRAM)}
          >
            DIAGRAM
          </Button>

          <Button
            size="small"
            variant={activeSection === SECTIONS.CLOUD_DIAGRAM ? "contained" : "outlined"}
            onClick={() => setActiveSection(SECTIONS.CLOUD_DIAGRAM)}
          >
            CLOUD DIAGRAM
          </Button>
        </Box>
      </Paper>

      {/* TASK 1 */}
      {activeSection === SECTIONS.TASK1 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            1️⃣ — Normalized Requirement Understanding
          </Typography>

          <Box
            component="pre"
            sx={{
              backgroundColor: "#1e1e1e",
              color: "#d4d4d4",
              p: 2,
              borderRadius: 1,
              overflow: "auto",
              fontSize: "0.875rem",
            }}
          >
            {JSON.stringify(solution.task_1_normalize_requirement, null, 2)}
          </Box>
        </Paper>
      )}

      {/* TASK 2 */}
      {activeSection === SECTIONS.TASK2 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            2️⃣ - Platform Architecture (High Level)
          </Typography>

          <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
            {solution.task_2_platform_architecture_high_level || "No output"}
          </Typography>
        </Paper>
      )}

      {/* TASK 3 */}
      {activeSection === SECTIONS.TASK3 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            3️⃣ — Architecture Flow Diagram (Text View)
          </Typography>

          <Box
            component="pre"
            sx={{
              backgroundColor: "#1e1e1e",
              color: "#d4d4d4",
              p: 2,
              borderRadius: 1,
              overflow: "auto",
              fontSize: "0.875rem",
            }}
          >
            {solution.task_3_architecture_flow_diagram_text_view || "No output"}
          </Box>
        </Paper>
      )}

      {/* TASK 4 */}
      {activeSection === SECTIONS.TASK4 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            4️⃣ — Best Architecture Recommendation
          </Typography>

          <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
            {solution.task_4_best_architecture_recommendation || "No output"}
          </Typography>
        </Paper>
      )}

      {/* TASK 5 */}
      {activeSection === SECTIONS.TASK5 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            5️⃣ — Key Design Decisions
          </Typography>

          <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
            {solution.task_5_key_design_decisions || "No output"}
          </Typography>
        </Paper>
      )}

      {/* TASK 6 Components */}
      {activeSection === SECTIONS.COMPONENTS && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <ExtensionIcon sx={{ mr: 1 }} />
            <Typography variant="h6">6️⃣ TASK 6 — Components</Typography>
          </Box>

          {(solution.task_6_components || []).map((component, index) => (
            <Card key={index} sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🔹 {component.name}{" "}
                  <Chip label={component.type} size="small" sx={{ ml: 1 }} />
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  ☁️ Service: <strong>{component.cloud_service || "N/A"}</strong>
                </Typography>
                <Typography variant="body2">
                  📄 {component.description || "No description"}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Paper>
      )}

      {/* TASK 7 Mermaid */}
      {activeSection === SECTIONS.DIAGRAM && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              mb: 2,
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <AccountTreeIcon sx={{ mr: 1 }} />
              <Typography variant="h6">7️⃣ TASK 7 — Mermaid Diagram</Typography>
            </Box>

            {solution.task_7_mermaid_diagram && (
              <Box sx={{ display: "flex", gap: 1 }}>
                <Button
                  size="small"
                  startIcon={<ContentCopyIcon />}
                  onClick={handleCopyDiagram}
                  variant="outlined"
                >
                  {copySuccess ? "Copied!" : "Copy Code"}
                </Button>

                <Button
                  size="small"
                  endIcon={
                    <ExpandMoreIcon
                      sx={{
                        transform: showRawDiagram
                          ? "rotate(180deg)"
                          : "rotate(0deg)",
                        transition: "0.3s",
                      }}
                    />
                  }
                  onClick={() => setShowRawDiagram(!showRawDiagram)}
                  variant="outlined"
                >
                  {showRawDiagram ? "Hide" : "Show"} Raw Code
                </Button>
              </Box>
            )}
          </Box>

          {diagramError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Mermaid Error: {diagramError}
            </Alert>
          )}

          <Collapse in={showRawDiagram}>
            <Box
              component="pre"
              sx={{
                backgroundColor: "#1e1e1e",
                color: "#d4d4d4",
                p: 2,
                borderRadius: 1,
                overflow: "auto",
                fontSize: "0.875rem",
                mb: 2,
                maxHeight: "300px",
              }}
            >
              {solution.task_7_mermaid_diagram}
            </Box>
          </Collapse>

          <Box
            ref={diagramRef}
            sx={{
              display: "flex",
              justifyContent: "center",
              p: 2,
              backgroundColor: "#ffffff",
              borderRadius: 1,
              overflow: "auto",
              minHeight: diagramError ? "100px" : "200px",
              "& svg": { maxWidth: "100%", height: "auto" },
            }}
          />
        </Paper>
      )}

      {/* Cloud Diagram */}
      {activeSection === SECTIONS.CLOUD_DIAGRAM && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <ArchitectureIcon sx={{ mr: 1 }} />
            <Typography variant="h6">☁️ Cloud Diagram (Icons)</Typography>
          </Box>

          <Box
            ref={cloudDiagramRef}
            sx={{
              width: "100%",
              maxWidth: "900px",
              margin: "0 auto",
              backgroundColor: "#ffffff",
              borderRadius: 2,
              border: "1px solid #e5e7eb",
              p: 1.5,

              overflowX: "auto",
              overflowY: "hidden",

              display: "flex",
              justifyContent: "center",
              alignItems: "center",

              "& svg": {
                maxWidth: "100%",
                height: "auto",
                display: "block",
              },

              // reduce node box size globally
              "& .node rect, & .node polygon": {
                rx: "6px",
                ry: "6px",
              },

              "& .label": {
                fontSize: "10px !important",
              },
            }}
          />


        </Paper>
      )}

      <Divider sx={{ my: 3 }} />
    </Box>
  );
};

export default SolutionDisplay;