from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

BASE = "/Users/bsmith/Documents/AI Training/vt_agentic_ai/4 - llm_internals/project"

styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontSize=11, leading=16, alignment=TA_JUSTIFY)
heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=13, leading=18)


def build_pdf(filename, title, sections):
    doc = SimpleDocTemplate(f"{BASE}/{filename}", pagesize=LETTER,
                            leftMargin=inch, rightMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 0.3 * inch)]
    for header, paragraphs in sections:
        story.append(Paragraph(header, heading))
        story.append(Spacer(1, 0.1 * inch))
        for p in paragraphs:
            story.append(Paragraph(p, body))
            story.append(Spacer(1, 0.1 * inch))
        story.append(Spacer(1, 0.15 * inch))
    doc.build(story)
    print(f"Created {filename}")


# ── Document 1: Network Security Manual ───────────────────────────────────────
build_pdf("network_security_manual.pdf", "Network Security Operations Manual", [
    ("1. Introduction to Network Security", [
        "Network security encompasses the policies, procedures, and technologies used to protect the "
        "integrity, confidentiality, and accessibility of computer networks and data. As organisations "
        "grow increasingly reliant on digital infrastructure, robust security practices have become "
        "essential to protect against evolving cyber threats.",
        "This manual provides system administrators and security professionals with a comprehensive "
        "guide to designing, implementing, and maintaining a secure network environment. Topics range "
        "from fundamental firewall configuration to advanced intrusion detection strategies.",
    ]),
    ("2. Firewall Configuration", [
        "A firewall is the first line of defence in any network security architecture. Modern next-"
        "generation firewalls (NGFWs) perform deep packet inspection (DPI), application-layer "
        "filtering, and stateful connection tracking. When configuring a firewall, administrators "
        "should adhere to the principle of least privilege: deny all traffic by default and allow only "
        "explicitly required communication paths.",
        "Rule ordering is critical. Firewalls evaluate rules top-to-bottom and stop at the first match. "
        "Specific allow rules should precede broad deny rules. Regularly audit and prune stale rules "
        "to reduce the attack surface. Logging should be enabled on all deny rules to capture "
        "reconnaissance attempts and anomalous traffic patterns.",
        "Zone-based segmentation separates the network into logical regions — DMZ, internal LAN, "
        "and management plane — each governed by distinct policy sets. Traffic crossing zone boundaries "
        "must be explicitly permitted, minimising lateral movement in the event of a breach.",
    ]),
    ("3. Intrusion Detection and Prevention Systems", [
        "Intrusion Detection Systems (IDS) monitor network traffic for signatures of known attacks and "
        "anomalous behaviour patterns. An Intrusion Prevention System (IPS) extends this capability by "
        "actively blocking identified threats in real time. Both systems rely on signature databases "
        "that must be updated continuously to address newly discovered vulnerabilities.",
        "Anomaly-based detection establishes a baseline of normal network behaviour and alerts on "
        "deviations. While more effective against zero-day attacks than signature-only approaches, "
        "anomaly engines require careful tuning to keep false-positive rates manageable. Machine "
        "learning models trained on labelled traffic datasets are increasingly used to improve accuracy.",
        "Placement of sensors matters. Inline IPS sensors between the firewall and core switches "
        "inspect north-south traffic, while lateral sensor deployment captures east-west flows between "
        "internal segments — a common vector for ransomware propagation.",
    ]),
    ("4. VPN and Encrypted Tunnels", [
        "Virtual Private Networks (VPNs) extend a private network across a public medium by "
        "encapsulating traffic in encrypted tunnels. IPsec and TLS/SSL are the dominant protocols. "
        "IPsec operates at the network layer and is suited for site-to-site connectivity, while "
        "TLS-based solutions such as OpenVPN and WireGuard are preferred for remote-access scenarios.",
        "WireGuard has gained rapid adoption due to its minimal codebase (~4,000 lines versus OpenVPN's "
        "~70,000), which reduces the audit surface and improves performance. Its use of modern "
        "cryptographic primitives — Curve25519, ChaCha20-Poly1305, BLAKE2 — provides strong security "
        "with lower computational overhead than legacy IPsec cipher suites.",
        "Always enforce certificate-based mutual authentication rather than pre-shared keys for "
        "production deployments. Rotate certificates annually and revoke compromised credentials "
        "immediately via a maintained Certificate Revocation List (CRL) or OCSP responder.",
    ]),
    ("5. Incident Response Procedures", [
        "A well-defined Incident Response Plan (IRP) reduces the mean time to detect (MTTD) and mean "
        "time to respond (MTTR) to security events. The six phases of the NIST incident response "
        "lifecycle are: Preparation, Detection and Analysis, Containment, Eradication, Recovery, and "
        "Post-Incident Activity.",
        "During containment, isolate affected systems by removing them from the network while "
        "preserving forensic evidence. Memory dumps and disk images should be captured before "
        "remediation to support root-cause analysis. Chain-of-custody documentation is mandatory "
        "if legal proceedings are anticipated.",
        "Post-incident reviews must produce actionable findings. Update detection rules, patch "
        "exploited vulnerabilities, and revise the IRP based on lessons learned. Tabletop exercises "
        "conducted quarterly help teams internalise procedures before a real incident occurs.",
    ]),
])

# ── Document 2: Climate Change Report ─────────────────────────────────────────
build_pdf("climate_change_report.pdf", "Annual Climate Change Impact Report 2025", [
    ("Executive Summary", [
        "Global average surface temperatures in 2024 exceeded pre-industrial baselines by 1.45 °C, "
        "placing the world perilously close to the 1.5 °C threshold established by the Paris Agreement. "
        "This report synthesises observational data, climate model projections, and socioeconomic "
        "impact assessments to inform policy decisions for the coming decade.",
        "Key findings indicate accelerating ice-sheet loss in Greenland and West Antarctica, record "
        "ocean heat content through the full water column, and a statistically significant increase "
        "in the frequency and intensity of extreme precipitation events across all inhabited continents.",
    ]),
    ("1. Atmospheric CO₂ Concentrations", [
        "Monthly mean CO₂ concentration at Mauna Loa Observatory reached 424.3 ppm in May 2024, "
        "representing a year-on-year increase of 2.8 ppm. The decadal growth rate has accelerated "
        "from 1.5 ppm/year in the 1990s to 2.5 ppm/year in the 2020s, driven by continued fossil-"
        "fuel combustion and land-use change, partially offset by natural carbon sinks.",
        "Permafrost thaw in Arctic regions is emerging as a significant positive feedback loop. "
        "Decomposition of organic matter previously locked in frozen soils releases methane (CH₄), "
        "a greenhouse gas with a 20-year global warming potential 86 times that of CO₂. Current "
        "Earth system models may underestimate permafrost emissions by up to 40%.",
    ]),
    ("2. Sea Level Rise and Coastal Impacts", [
        "Global mean sea level rose 3.7 mm in 2024, bringing the cumulative rise since 1993 to "
        "approximately 112 mm. Thermal expansion of warming ocean water accounts for roughly 40% of "
        "this increase, while the remainder stems from land-ice melt. Under RCP 8.5 scenarios, "
        "sea levels could rise between 0.61 m and 1.10 m by 2100.",
        "Low-lying coastal megacities — including Miami, Jakarta, Mumbai, and Shanghai — face "
        "compounding risks from sea-level rise, storm surge intensification, and saltwater intrusion "
        "into freshwater aquifers. The economic cost of unmitigated coastal flooding is projected to "
        "reach USD 14.2 trillion annually by 2100 under a business-as-usual emissions trajectory.",
        "Managed retreat strategies, nature-based defences such as mangrove restoration, and engineered "
        "solutions including seawalls and surge barriers must be deployed in complementary combinations "
        "tailored to local geomorphology, population density, and financial capacity.",
    ]),
    ("3. Extreme Weather Events", [
        "The attribution science linking anthropogenic climate change to specific extreme weather events "
        "has matured substantially. In 2024, 23 of 28 peer-reviewed rapid attribution studies found "
        "that human-caused warming made the studied event more likely or more intense, with median "
        "probability ratios exceeding 2.0 for heatwaves and heavy precipitation episodes.",
        "Tropical cyclone intensification rates have increased. The proportion of storms reaching "
        "Category 4–5 intensity has grown by approximately 25% since the 1980s. Rapid intensification "
        "events — defined as a wind speed increase of at least 35 knots in 24 hours — have become "
        "more frequent in the Atlantic and Western Pacific basins, complicating evacuation planning.",
    ]),
    ("4. Mitigation and Adaptation Strategies", [
        "Achieving net-zero emissions by 2050 requires an immediate tripling of renewable energy "
        "capacity additions, electrification of heating and transport, and deployment of carbon dioxide "
        "removal (CDR) technologies at gigaton scale. Bioenergy with carbon capture and storage (BECCS) "
        "and direct air capture (DAC) are the leading CDR approaches, though both face significant "
        "land-use, energy, and cost constraints at the scales required.",
        "Adaptation investment remains critically underfunded. The UN Environment Programme estimates "
        "that developing nations require USD 387 billion annually for adaptation by 2030, yet current "
        "international climate finance flows for adaptation total only USD 63 billion per year. "
        "Closing this gap is both a moral imperative and an economic necessity, as every dollar invested "
        "in resilient infrastructure returns an estimated USD 6 in avoided disaster losses.",
    ]),
])

# ── Document 3: Machine Learning Fundamentals ─────────────────────────────────
build_pdf("ml_fundamentals_guide.pdf", "Machine Learning Fundamentals: A Practitioner's Guide", [
    ("1. Introduction to Machine Learning", [
        "Machine learning (ML) is a subfield of artificial intelligence in which algorithms learn "
        "patterns from data rather than following explicitly programmed rules. The field encompasses "
        "supervised learning, unsupervised learning, semi-supervised learning, and reinforcement "
        "learning — each suited to different problem structures and data availability scenarios.",
        "The modern ML workflow consists of five stages: data collection and cleaning, feature "
        "engineering, model selection and training, evaluation, and deployment. Neglecting any stage "
        "degrades overall system performance. In practice, data quality and feature design account "
        "for a greater share of model performance variance than architecture choice alone.",
    ]),
    ("2. Supervised Learning Algorithms", [
        "Supervised learning trains a model on labelled examples to predict outputs for unseen inputs. "
        "Linear regression models continuous targets by fitting a hyperplane to minimise mean squared "
        "error (MSE). Logistic regression extends this to binary classification via the sigmoid "
        "activation, producing calibrated probability estimates.",
        "Decision trees partition the feature space through recursive binary splits, choosing splits "
        "that maximise information gain or Gini impurity reduction. Ensemble methods — Random Forests "
        "and Gradient Boosted Trees (e.g., XGBoost, LightGBM) — combine many weak trees to achieve "
        "state-of-the-art performance on tabular data. Gradient boosting builds trees sequentially, "
        "each correcting the residual errors of its predecessors.",
        "Support Vector Machines (SVMs) find the maximum-margin hyperplane separating classes in a "
        "transformed feature space defined by a kernel function. The radial basis function (RBF) "
        "kernel maps inputs to an infinite-dimensional space, enabling non-linear decision boundaries "
        "with computational efficiency via the kernel trick.",
    ]),
    ("3. Neural Networks and Deep Learning", [
        "Artificial neural networks are composed of layers of interconnected nodes (neurons) that "
        "apply learned affine transformations followed by non-linear activation functions. Stacking "
        "many such layers — deep learning — enables the extraction of hierarchical feature "
        "representations directly from raw input data such as pixels, audio waveforms, or tokens.",
        "Backpropagation computes the gradient of the loss function with respect to all network "
        "parameters by applying the chain rule through the computational graph. Stochastic gradient "
        "descent (SGD) and its adaptive variants — Adam, AdamW, RMSProp — use these gradients to "
        "iteratively update weights. Batch normalisation, dropout, and residual connections address "
        "training instability and vanishing gradient problems in very deep networks.",
        "Transformer architectures, introduced in the 2017 paper 'Attention Is All You Need', have "
        "become the dominant paradigm for natural language processing. The self-attention mechanism "
        "computes pairwise relationships between all tokens in a sequence, enabling the model to "
        "capture long-range dependencies without the sequential bottleneck of recurrent networks.",
    ]),
    ("4. Model Evaluation and Validation", [
        "Proper evaluation prevents over-fitting to the training distribution. The standard approach "
        "partitions data into training, validation, and test sets. The training set fits model "
        "parameters; the validation set guides hyperparameter selection; the test set provides an "
        "unbiased performance estimate. Data leakage — allowing information from the test set to "
        "influence any earlier stage — is a pervasive source of inflated benchmark results.",
        "Classification metrics include accuracy, precision, recall, F1-score, and area under the "
        "ROC curve (AUC-ROC). For imbalanced datasets, accuracy is misleading; precision-recall "
        "curves and the Matthews Correlation Coefficient (MCC) provide more informative summaries. "
        "Regression metrics include MSE, RMSE, mean absolute error (MAE), and R².",
        "k-Fold cross-validation partitions data into k equal folds, training k models each using a "
        "different fold as the validation set. The mean and standard deviation of fold scores estimate "
        "generalisation performance and its variance. Stratified k-fold preserves class proportions "
        "across folds, which is essential for imbalanced classification problems.",
    ]),
    ("5. Retrieval-Augmented Generation", [
        "Retrieval-Augmented Generation (RAG) combines a dense retrieval system with a large language "
        "model (LLM) to ground generated responses in relevant source documents. A query encoder maps "
        "the user's question to a dense vector; an approximate nearest-neighbour index such as FAISS "
        "retrieves the top-k most similar document chunks; and the LLM generates an answer conditioned "
        "on both the query and the retrieved context.",
        "Chunking strategy critically affects retrieval quality. Fixed-size character windows are "
        "simple but may split sentences mid-thought. Sentence or paragraph-level chunking respects "
        "linguistic boundaries but produces variable-length chunks. Recursive character text splitters "
        "attempt to split on paragraph, then sentence, then word boundaries, balancing coherence and "
        "uniformity. Chunk overlap — repeating tokens at boundaries — helps preserve context across "
        "adjacent chunks.",
        "Embedding model choice affects both retrieval precision and computational cost. OpenAI's "
        "text-embedding-3-small model produces 1,536-dimensional vectors and offers a strong quality-"
        "cost balance for most RAG applications. Re-ranking with a cross-encoder after initial "
        "retrieval further improves precision by scoring query-chunk pairs jointly rather than "
        "independently.",
    ]),
])
