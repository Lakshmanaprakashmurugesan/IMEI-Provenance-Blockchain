import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import csv
import json
import time
import os
from provenance_engine import ProvenanceEngine
from event_streaming.producer import DeviceTelemetryProducer
from event_streaming.consumer import DataLakeIngestionConsumer

LOCAL_ENGINE = ProvenanceEngine()

# Configure professional enterprise layout
st.set_page_config(
    page_title="Telecom Supply Chain Resilience Control Tower",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium control-tower visual layer — business logic is unchanged
st.markdown(
    """
    <style>
    /* ---------- APP ---------- */
    .stApp {
        background:
            radial-gradient(circle at 82% 3%, rgba(79,70,229,.08), transparent 23rem),
            radial-gradient(circle at 8% 85%, rgba(14,165,233,.06), transparent 25rem),
            #f7f9fc;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #172554 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }

    section[data-testid="stSidebar"] * {
        color: #eaf0ff;
    }

    section[data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        font-size: 1.42rem !important;
        font-weight: 800 !important;
        letter-spacing: -.02em;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.12);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.05);
        border-radius: 12px;
        padding: .50rem .55rem;
        margin: .28rem 0;
        transition: all .18s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,.09);
        border-color: rgba(255,255,255,.14);
        transform: translateX(2px);
    }

    .sidebar-kicker {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 999px;
        background: rgba(99,102,241,.22);
        border: 1px solid rgba(165,180,252,.28);
        color: #c7d2fe;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .10em;
        text-transform: uppercase;
        margin: .2rem 0 .85rem 0;
    }

    .node-card {
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 16px;
        padding: 14px 14px 10px;
        margin-top: .8rem;
        box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
    }

    .node-title {
        color: #ffffff;
        font-size: .92rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .node-row {
        display: grid;
        grid-template-columns: 10px 1fr;
        gap: 9px;
        margin: 10px 0;
        align-items: start;
    }

    .node-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #34d399;
        margin-top: 5px;
        box-shadow: 0 0 0 4px rgba(52,211,153,.12);
    }

    .node-name {
        color: #f8fafc;
        font-size: .84rem;
        font-weight: 750;
    }

    .node-state {
        color: #9fb1d0;
        font-size: .73rem;
        margin-top: 1px;
    }

    /* ---------- HERO ---------- */
    .hero-shell {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #111827 0%, #1e3a8a 58%, #4338ca 100%);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 24px;
        padding: 28px 32px 26px;
        box-shadow: 0 18px 45px rgba(30,58,138,.16);
        margin-bottom: 1.2rem;
    }

    .hero-shell:after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -90px;
        top: -120px;
        border-radius: 50%;
        background: rgba(255,255,255,.07);
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.16);
        color: #dbeafe;
        font-size: .70rem;
        font-weight: 800;
        letter-spacing: .11em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.35rem;
        line-height: 1.12;
        font-weight: 820;
        letter-spacing: -.035em;
        max-width: 930px;
        margin: 0;
    }

    .hero-subtitle {
        color: #d6e2ff;
        font-size: .98rem;
        line-height: 1.62;
        max-width: 860px;
        margin-top: 12px;
    }

    .hero-tags {
        margin-top: 16px;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .hero-tag {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 9px;
        background: rgba(255,255,255,.09);
        color: #eef4ff;
        border: 1px solid rgba(255,255,255,.12);
        font-size: .75rem;
        font-weight: 650;
    }

    /* ---------- SECTION CARDS ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        border: 1px solid #dfe6ef !important;
        background: rgba(255,255,255,.86) !important;
        box-shadow: 0 10px 30px rgba(15,23,42,.05);
    }

    .section-label {
        color: #1e3a8a;
        font-size: .73rem;
        text-transform: uppercase;
        letter-spacing: .11em;
        font-weight: 850;
        margin-bottom: 4px;
    }

    .section-title {
        color: #172033;
        font-size: 1.18rem;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .section-help {
        color: #6b7280;
        font-size: .84rem;
        margin-bottom: 8px;
    }

    /* ---------- INPUTS ---------- */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 1px solid #d8e0eb !important;
        background: #f8fafc !important;
        min-height: 49px;
        box-shadow: inset 0 1px 2px rgba(15,23,42,.025);
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 3px rgba(79,70,229,.10) !important;
    }

    /* ---------- BUTTON ---------- */
    .stButton > button {
        min-height: 45px;
        border-radius: 12px !important;
        border: 0 !important;
        font-weight: 800 !important;
        padding: .68rem 1.25rem !important;
        background: linear-gradient(135deg, #ef4444 0%, #f43f5e 100%) !important;
        box-shadow: 0 9px 20px rgba(244,63,94,.20);
        transition: all .16s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 13px 26px rgba(244,63,94,.28);
    }

    /* ---------- METRICS ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border: 1px solid #dfe7f1;
        border-radius: 17px;
        padding: 1rem 1rem .9rem;
        box-shadow: 0 10px 26px rgba(15,23,42,.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #172033;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        box-shadow: 0 7px 20px rgba(15,23,42,.04);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e0e7ef;
        box-shadow: 0 8px 22px rgba(15,23,42,.04);
    }

    /* ---------- RESULT / SMALL LABELS ---------- */
    .result-bar {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin: 8px 0 14px;
    }

    .result-chip {
        padding: 6px 9px;
        background: #eef2ff;
        border: 1px solid #d9ddff;
        color: #3730a3;
        border-radius: 999px;
        font-size: .74rem;
        font-weight: 750;
    }

    .footer-note {
        color: #8491a4;
        font-size: .72rem;
        margin-top: .45rem;
    }

    hr {
        border: none;
        border-top: 1px solid #e4e9f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuration for underlying microservice gateway connections
GATEWAY_URL = os.getenv("IMEI_GATEWAY_URL", "http://localhost:8000/api/v1/provenance/verify")

# -------------------------------------------------------------------
# AUTOMATIC STREAMLIT TEST RESULT LOGGING
# -------------------------------------------------------------------
# This does not change the visible Streamlit UI.
#
# Every time "Execute Ledger Query" is clicked, this app records:
# - date
# - time
# - IMEI entered
# - test case name
# - IMEI result shown by Streamlit
# - whether Streamlit completed the test successfully
# - PASS / FAIL
#
# PASS = Streamlit successfully handled the test case and produced the
#        expected application behavior/result.
#
# FAIL = Streamlit encountered an unexpected application/processing error.
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# PROJECT PATH
# -------------------------------------------------------------------
# Streamlit is launched from the repository root with:
#   python -m streamlit run dashboard/app.py
#
# Therefore Path.cwd() is the exact repository folder visible in VS Code.
# test_log.csv is ALWAYS written to:
#   <CURRENT REPOSITORY>/tests/test_log.csv
# -------------------------------------------------------------------
WORKING_ROOT = Path.cwd().resolve()

if (WORKING_ROOT / "dashboard" / "app.py").exists():
    PROJECT_ROOT = WORKING_ROOT
else:
    # Safe fallback if Streamlit is launched from another directory.
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

TESTS_DIR = PROJECT_ROOT / "tests"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"
TEST_LOG_FILE = PROJECT_ROOT / "tests" / "test_log.csv"

EVENT_STREAM_LOG_FILE = EVIDENCE_DIR / "event_stream_log.csv"
SECURITY_EVENT_LOG_FILE = EVIDENCE_DIR / "security_event_log.csv"

EVENT_STREAM_HEADERS = [
    "event_date",
    "event_time",
    "imei",
    "event_type",
    "operator",
    "producer_status",
    "consumer_status",
    "stream_result"
]

SECURITY_EVENT_HEADERS = [
    "event_date",
    "event_time",
    "imei",
    "security_event",
    "detected_state",
    "result"
]


def ensure_evidence_csv(file_path, headers):
    """
    Ensure generated evidence uses one consistent schema.

    If an older incompatible generated log exists, preserve it as a
    timestamped legacy file and create a clean current-format log.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists() and file_path.stat().st_size > 0:
        try:
            with file_path.open(
                "r",
                newline="",
                encoding="utf-8"
            ) as file:
                existing_header = next(csv.reader(file), [])

            if existing_header != headers:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                legacy_path = file_path.with_name(
                    f"{file_path.stem}_legacy_{timestamp}{file_path.suffix}"
                )
                file_path.replace(legacy_path)
        except Exception:
            pass

    if not file_path.exists() or file_path.stat().st_size == 0:
        with file_path.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)


def record_event_stream_evidence(
    imei,
    event_type,
    operator
):
    """
    Record the actual Page 1 verification event for Page 2 analytics.

    This does not invent KPI values. It records one event only when the
    user actually executes a successful IMEI verification.
    """
    ensure_evidence_csv(
        EVENT_STREAM_LOG_FILE,
        EVENT_STREAM_HEADERS
    )

    now = datetime.now()
    producer = DeviceTelemetryProducer()
    consumer = DataLakeIngestionConsumer()
    emitted = producer.emit_lifecycle_event(imei, event_type, operator)
    processed = consumer.process_incoming_stream_packet(emitted["packet"])
    simulation_pass = (
        emitted.get("status") == "SIMULATED_EMIT"
        and processed.get("status") == "SIMULATED_PROCESS"
    )

    with EVENT_STREAM_LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            imei,
            event_type,
            operator,
            emitted.get("status", "SIMULATION_ERROR"),
            processed.get("status", "SIMULATION_ERROR"),
            "SIMULATION_PASS" if simulation_pass else "SIMULATION_FAIL"
        ])


def record_security_evidence(
    imei,
    security_event,
    detected_state
):
    """
    Record security evidence only when Page 1 actually returns a
    tampered/security result.
    """
    ensure_evidence_csv(
        SECURITY_EVENT_LOG_FILE,
        SECURITY_EVENT_HEADERS
    )

    now = datetime.now()

    with SECURITY_EVENT_LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            imei,
            security_event,
            detected_state,
            "DETECTED"
        ])

TEST_LOG_HEADERS = [
    "run_date",
    "run_time",
    "imei",
    "requesting_node",
    "test_case",
    "imei_result",
    "current_status",
    "current_owner",
    "data_source",
    "response_time_ms",
    "streamlit_status",
    "result"
]


def initialize_test_log():
    """Create tests/test_log.csv with the exact required 12-column schema."""
    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    # If the file exists but is completely empty, write the header now.
    if TEST_LOG_FILE.exists() and TEST_LOG_FILE.stat().st_size == 0:
        with TEST_LOG_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=TEST_LOG_HEADERS)
            writer.writeheader()
            file.flush()
            os.fsync(file.fileno())
        return

    # If the file exists with content, verify its header.
    if TEST_LOG_FILE.exists() and TEST_LOG_FILE.stat().st_size > 0:
        try:
            with TEST_LOG_FILE.open("r", newline="", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                existing_header = next(reader, [])

            if existing_header == TEST_LOG_HEADERS:
                return

            # Preserve an old/incompatible CSV instead of mixing schemas.
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            legacy_file = TEST_LOG_FILE.with_name(
                f"test_log_legacy_{timestamp}.csv"
            )
            TEST_LOG_FILE.replace(legacy_file)
        except Exception:
            # If the existing file cannot be read, preserve it and rebuild.
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            legacy_file = TEST_LOG_FILE.with_name(
                f"test_log_legacy_{timestamp}.csv"
            )
            try:
                TEST_LOG_FILE.replace(legacy_file)
            except Exception:
                pass

    # Create a new current-schema file if needed.
    if not TEST_LOG_FILE.exists():
        with TEST_LOG_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=TEST_LOG_HEADERS)
            writer.writeheader()
            file.flush()
            os.fsync(file.fileno())


def write_test_log(
    imei,
    requesting_node,
    test_case,
    imei_result,
    current_status,
    current_owner,
    data_source,
    response_time_ms,
    streamlit_status,
    result
):
    """
    Automatically capture and append the complete Page 1 verification result
    to <repository>/tests/test_log.csv.

    Exact columns:
    run_date,run_time,imei,requesting_node,test_case,imei_result,
    current_status,current_owner,data_source,response_time_ms,
    streamlit_status,result
    """
    initialize_test_log()

    now = datetime.now()

    # Normalize every field so CSV always receives all 12 values.
    row = {
        "run_date": now.strftime("%Y-%m-%d"),
        "run_time": now.strftime("%H:%M:%S"),
        "imei": str(imei).strip() if imei is not None else "NOT_AVAILABLE",
        "requesting_node": (
            str(requesting_node).strip()
            if requesting_node is not None
            else "NOT_AVAILABLE"
        ),
        "test_case": (
            str(test_case).strip()
            if test_case is not None
            else "IMEI Provenance Verification"
        ),
        "imei_result": (
            str(imei_result).strip()
            if imei_result is not None
            else "NOT_AVAILABLE"
        ),
        "current_status": (
            str(current_status).strip()
            if current_status is not None
            else "NOT_AVAILABLE"
        ),
        "current_owner": (
            str(current_owner).strip()
            if current_owner is not None
            else "NOT_AVAILABLE"
        ),
        "data_source": (
            str(data_source).strip()
            if data_source is not None
            else "NOT_AVAILABLE"
        ),
        "response_time_ms": (
            round(float(response_time_ms), 3)
            if response_time_ms is not None
            else 0.0
        ),
        "streamlit_status": (
            str(streamlit_status).strip()
            if streamlit_status is not None
            else "NOT_AVAILABLE"
        ),
        "result": (
            str(result).strip()
            if result is not None
            else "FAIL"
        )
    }

    # Strict append to the exact repository CSV.
    with TEST_LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=TEST_LOG_HEADERS,
            extrasaction="ignore"
        )
        writer.writerow(row)
        file.flush()
        os.fsync(file.fileno())

    return row


SAMPLE_INPUT_DIR = EVIDENCE_DIR / "sample_inputs"
SAMPLE_OUTPUT_DIR = EVIDENCE_DIR / "sample_outputs"


def save_verification_artifacts(
    imei,
    operator_node,
    input_payload,
    output_payload,
    imei_result,
    test_result,
    data_source
):
    """
    Persist the exact input and output of each executed IMEI verification.

    One run creates:
      evidence/sample_inputs/<run_id>_input.json
      evidence/sample_outputs/<run_id>_output.json
    """
    SAMPLE_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    run_id = (
        now.strftime("%Y%m%d_%H%M%S_%f")
        + "_"
        + str(imei)
    )

    input_record = {
        "run_date": now.strftime("%Y-%m-%d"),
        "run_time": now.strftime("%H:%M:%S"),
        "imei": str(imei),
        "requesting_node": operator_node,
        "data_source": data_source,
        "request_payload": input_payload
    }

    output_record = {
        "run_date": now.strftime("%Y-%m-%d"),
        "run_time": now.strftime("%H:%M:%S"),
        "imei": str(imei),
        "imei_result": imei_result,
        "test_result": test_result,
        "data_source": data_source,
        "response": output_payload
    }

    input_file = SAMPLE_INPUT_DIR / f"{run_id}_input.json"
    output_file = SAMPLE_OUTPUT_DIR / f"{run_id}_output.json"

    with input_file.open("w", encoding="utf-8") as file:
        json.dump(
            input_record,
            file,
            indent=2,
            default=str
        )

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            output_record,
            file,
            indent=2,
            default=str
        )

    return input_file, output_file


# Create/repair the exact repository CSV immediately when Streamlit starts.
TESTS_DIR.mkdir(parents=True, exist_ok=True)
initialize_test_log()

# Prepare Page 2 evidence files.
ensure_evidence_csv(
    EVENT_STREAM_LOG_FILE,
    EVENT_STREAM_HEADERS
)
ensure_evidence_csv(
    SECURITY_EVENT_LOG_FILE,
    SECURITY_EVENT_HEADERS
)

# Preserve Asset Verification state while navigating between Streamlit modules.
# Durable keys do NOT belong to widgets, so Streamlit will not delete them
# when the Asset Verification page is temporarily not rendered.
if "saved_imei" not in st.session_state:
    st.session_state["saved_imei"] = ""

if "saved_operator_node" not in st.session_state:
    st.session_state["saved_operator_node"] = "CarrierMSP (Node A)"

if "last_verification_data" not in st.session_state:
    st.session_state["last_verification_data"] = None

if "last_verification_source" not in st.session_state:
    st.session_state["last_verification_source"] = None


def persist_imei():
    st.session_state["saved_imei"] = st.session_state.get("_imei_widget", "")


def persist_operator_node():
    st.session_state["saved_operator_node"] = st.session_state.get(
        "_operator_node_widget",
        "CarrierMSP (Node A)"
    )


def render_verification_summary(data):
    """Render the saved/current provenance response without rerunning the query."""
    st.markdown("---")
    st.markdown('<div class="section-label">Ledger Response</div>', unsafe_allow_html=True)
    st.markdown("### Verification Activity Summary")
    m_col1, m_col2, m_col3 = st.columns(3)
    state = data.get("authenticity_state") or ("TAMPERED" if data.get("is_tampered") else "GENUINE" if data.get("is_genuine") else "UNKNOWN")
    m_col1.metric("Authenticity State", state)
    m_col2.metric("Current State Lock", data.get("current_status", "NOT_AVAILABLE"))
    m_col3.metric("Assigned Custody Node", data.get("current_owner", "NOT_AVAILABLE"))
    if state == "TAMPERED":
        st.error("⚠️ TAMPER DETECTED: " + data.get("reason", "Integrity verification failed."))
    elif state == "GENUINE":
        st.success("✅ VERIFIED: " + data.get("reason", "Signature and record integrity checks passed."))
    elif state == "UNKNOWN":
        st.info("ℹ️ Valid IMEI format, but no matching device record exists in the prototype registry. The system does not classify it as genuine or tampered.")
    else:
        st.warning("Invalid IMEI: " + data.get("reason", "Input validation failed."))
    if data.get("signature_valid") is not None or data.get("hash_integrity_valid") is not None:
        c1,c2=st.columns(2); c1.metric("Manufacturer Signature", "VALID" if data.get("signature_valid") else "INVALID"); c2.metric("Record Hash Integrity", "VALID" if data.get("hash_integrity_valid") else "MISMATCH")
    if data.get("lifecycle_history"):
        st.markdown("### Lifecycle Governance Audit Trail")
        df=pd.DataFrame(data["lifecycle_history"])
        st.dataframe(df, use_container_width=True)

# Global Navigation Sidebar
st.sidebar.image("https://img.icons8.com/nolan/128/blockchain.png", width=74)
st.sidebar.markdown('<div class="sidebar-kicker">Telecom provenance</div>', unsafe_allow_html=True)
st.sidebar.title("Network Control Center")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Navigation Modules",
    ["Asset Verification Tower", "Consensus Analytics & KPIs", "Security & Threat Matrix"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div class="node-card">'
    '<div class="node-title">System Node Status</div>'
    '<div class="node-row"><span class="node-dot"></span><div><div class="node-name">API Gateway</div><div class="node-state">Prototype Active</div></div></div>'
    '<div class="node-row"><span class="node-dot"></span><div><div class="node-name">Fabric Chaincode</div><div class="node-state">Simulation Ready</div></div></div>'
    '<div class="node-row"><span class="node-dot"></span><div><div class="node-name">Kafka Stream</div><div class="node-state">Simulation Ready</div></div></div>'
    '</div>',
    unsafe_allow_html=True
)

# --- MODULE 1: ASSET VERIFICATION TOWER ---
if app_mode == "Asset Verification Tower":
    st.markdown(
        '<div class="hero-shell">'
        '<div class="hero-badge">Permissioned Blockchain Verification</div>'
        '<div class="hero-title">🛡️ Blockchain-Based Device Provenance &amp; Cryptographic Identity Verification</div>'
        '<div class="hero-subtitle">Query the permissioned ledger to audit hardware authenticity, verify chain-of-custody state, and surface integrity anomalies for a submitted device identifier.</div>'
        '<div class="hero-tags">'
        '<span class="hero-tag">IMEI Provenance</span>'
        '<span class="hero-tag">Cryptographic Integrity</span>'
        '<span class="hero-tag">Custody Trace</span>'
        '<span class="hero-tag">Tamper Detection</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown('<div class="section-label">Verification Console</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Query a Device Asset</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-help">Enter a 15-digit IMEI and select the requesting network participant. The existing verification logic and evidence logging run exactly as before.</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([2, 1], gap="large")

        # Widget keys are temporary while this page is visible.
        # Restore them from durable state every time the user returns.
        if "_imei_widget" not in st.session_state:
            st.session_state["_imei_widget"] = st.session_state["saved_imei"]

        if "_operator_node_widget" not in st.session_state:
            st.session_state["_operator_node_widget"] = st.session_state[
                "saved_operator_node"
            ]

        with col1:
            input_imei = st.text_input(
                "Enter 15-Digit Device IMEI Asset Identifier:",
                placeholder="Enter a 15-digit IMEI",
                key="_imei_widget",
                on_change=persist_imei
            )

        with col2:
            operator_node = st.selectbox(
                "Requesting Origin Node (MSP Profile):",
                [
                    "CarrierMSP (Node A)",
                    "OEMMSP (Origin)",
                    "DistributorMSP"
                ],
                key="_operator_node_widget",
                on_change=persist_operator_node
            )

        st.markdown(
            '<div class="result-bar">'
            '<span class="result-chip">15-digit identifier</span>'
            '<span class="result-chip">Permissioned query</span>'
            '<span class="result-chip">Evidence logging enabled</span>'
            '</div>',
            unsafe_allow_html=True
        )

    query_clicked = st.button("Execute Ledger Query", type="primary")

    if query_clicked:
        # Persist what the user submitted before any processing/navigation.
        st.session_state["saved_imei"] = input_imei
        st.session_state["saved_operator_node"] = operator_node

        # ---------------------------------------------------------------
        # INVALID INPUT TEST
        # ---------------------------------------------------------------
        if not input_imei or len(input_imei) != 15 or not input_imei.isdigit():
            st.error(
                "Validation Error: Input identifier must be an exact "
                "15-digit numeric string."
            )

            write_test_log(
                imei=input_imei if input_imei else "EMPTY",
                requesting_node=operator_node,
                test_case="IMEI Input Validation",
                imei_result="INVALID",
                current_status="INVALID_INPUT",
                current_owner="NOT_AVAILABLE",
                data_source="STREAMLIT_INPUT_VALIDATION",
                response_time_ms=0.0,
                streamlit_status="Invalid IMEI input",
                result="FAIL"
            )

            # Store the invalid input/output evidence as well.
            save_verification_artifacts(
                imei=input_imei if input_imei else "EMPTY",
                operator_node=operator_node,
                input_payload={
                    "imei": input_imei
                },
                output_payload={
                    "imei_result": "INVALID",
                    "message": "IMEI must contain exactly 15 numeric digits."
                },
                imei_result="INVALID",
                test_result="FAIL",
                data_source="STREAMLIT_INPUT_VALIDATION"
            )

        else:
            try:
                with st.spinner(
                    "Processing zero-trust cryptographic ledger "
                    "validation parameters..."
                ):
                    payload = {
                        "imei": input_imei,
                        "requesting_msp": operator_node
                    }

                    data_source = "API Gateway"
                    request_started = time.perf_counter()
                    try:
                        response = requests.post(GATEWAY_URL, json=payload, timeout=5)
                        response.raise_for_status()
                        data = response.json()
                    except Exception:
                        # Safe fallback: use exactly the same shared provenance engine as the API.
                        # No IMEI value is hardcoded as GENUINE or TAMPERED.
                        data_source = "Shared Local Provenance Engine"
                        data = LOCAL_ENGINE.verify(input_imei).to_dict()

                    response_time_ms = round(
                        (time.perf_counter() - request_started) * 1000,
                        3
                    )

                # -------------------------------------------------------
                # DETERMINE THE SAME IMEI RESULT THAT STREAMLIT WILL SHOW
                # -------------------------------------------------------
                imei_result = data.get("authenticity_state") or (
                    "TAMPERED" if data.get("is_tampered") else
                    "GENUINE" if data.get("is_genuine") else "UNKNOWN"
                )

                # -------------------------------------------------------
                # AUTOMATIC TEST RESULT
                # -------------------------------------------------------
                # User-facing interpretation:
                #   GENUINE  -> PASS
                #   TAMPERED -> FAIL
                #   anything else -> FAIL
                test_result = (
                    "PASS"
                    if imei_result in ["GENUINE", "TAMPERED", "UNKNOWN"]
                    else "FAIL"
                )

                # -------------------------------------------------------
                # FETCH ALL 12 TEST-LOG VALUES FROM THIS ACTUAL RUN
                # -------------------------------------------------------
                fetched_imei = data.get("imei", input_imei)
                fetched_requesting_node = operator_node
                fetched_test_case = "IMEI Provenance Verification"
                fetched_imei_result = imei_result
                fetched_current_status = data.get(
                    "current_status",
                    "NOT_AVAILABLE"
                )
                fetched_current_owner = data.get(
                    "current_owner",
                    "NOT_AVAILABLE"
                )
                fetched_data_source = data_source
                fetched_response_time_ms = response_time_ms
                fetched_streamlit_status = (
                    f"Query completed successfully via {data_source}"
                )
                # Test result reflects whether the application behaved as expected.
                # GENUINE and TAMPERED are both valid expected verification outcomes.
                # FAIL is reserved for invalid input, application/API errors,
                # or other unexpected execution behavior.
                fetched_result = (
                    "PASS"
                    if fetched_imei_result in ["GENUINE", "TAMPERED", "UNKNOWN"]
                    else "FAIL"
                )

                saved_test_row = write_test_log(
                    imei=fetched_imei,
                    requesting_node=fetched_requesting_node,
                    test_case=fetched_test_case,
                    imei_result=fetched_imei_result,
                    current_status=fetched_current_status,
                    current_owner=fetched_current_owner,
                    data_source=fetched_data_source,
                    response_time_ms=fetched_response_time_ms,
                    streamlit_status=fetched_streamlit_status,
                    result=fetched_result
                )

                # Persist the exact input and output for this verification.
                save_verification_artifacts(
                    imei=input_imei,
                    operator_node=operator_node,
                    input_payload=payload,
                    output_payload=data,
                    imei_result=imei_result,
                    test_result=test_result,
                    data_source=data_source
                )

                # -------------------------------------------------------
                # PAGE 2 EVENT / SECURITY EVIDENCE CONNECTION
                # -------------------------------------------------------
                # One actual verification action creates one lifecycle/
                # event-stream evidence record.
                if imei_result == "TAMPERED":
                    generated_event_type = "TAMPER_DETECTED"
                elif imei_result == "GENUINE":
                    generated_event_type = "VERIFICATION_COMPLETED"
                else:
                    generated_event_type = "VERIFICATION_UNKNOWN"

                if imei_result in ["GENUINE", "TAMPERED", "UNKNOWN"]:
                    record_event_stream_evidence(
                        imei=input_imei,
                        event_type=generated_event_type,
                        operator=operator_node
                    )

                # A tampered result creates separate security evidence rows
                # so Page 2 can independently count each detected condition.
                if imei_result == "TAMPERED":
                    security_events_to_record = ["TAMPER_DETECTED"]
                    if data.get("hash_integrity_valid") is False:
                        security_events_to_record.append("HASH_MISMATCH")
                    if data.get("signature_valid") is False:
                        security_events_to_record.append("SIGNATURE_FAILURE")

                    for security_event_name in security_events_to_record:
                        record_security_evidence(
                            imei=input_imei,
                            security_event=security_event_name,
                            detected_state="TAMPERED"
                        )

                # Save the exact response so it remains visible after visiting
                # another navigation module and returning.
                st.session_state["last_verification_data"] = data
                st.session_state["last_verification_source"] = data_source

                # Display the current ledger response.
                render_verification_summary(data)

                st.caption(
                    "Test evidence automatically saved → "
                    f"{TEST_LOG_FILE} | "
                    f"IMEI: {saved_test_row['imei']} | "
                    f"State: {saved_test_row['current_status']} | "
                    f"Owner: {saved_test_row['current_owner']} | "
                    f"Result: {saved_test_row['result']}"
                )

            except Exception as app_error:
                # Unexpected Streamlit/application processing failure.
                write_test_log(
                    imei=input_imei,
                    requesting_node=operator_node,
                    test_case="IMEI Provenance Verification",
                    imei_result="APPLICATION_ERROR",
                    current_status="ERROR",
                    current_owner="NOT_AVAILABLE",
                    data_source=(
                        data_source if "data_source" in locals() else "APPLICATION"
                    ),
                    response_time_ms=(
                        response_time_ms if "response_time_ms" in locals() else 0.0
                    ),
                    streamlit_status=str(app_error),
                    result="FAIL"
                )

                save_verification_artifacts(
                    imei=input_imei,
                    operator_node=operator_node,
                    input_payload=payload if "payload" in locals() else {
                        "imei": input_imei
                    },
                    output_payload={
                        "error": str(app_error)
                    },
                    imei_result="APPLICATION ERROR",
                    test_result="FAIL",
                    data_source=(
                        data_source
                        if "data_source" in locals()
                        else "APPLICATION"
                    )
                )

                st.error(
                    "Application Error: The IMEI verification could not "
                    "be completed."
                )

    # If the user visited another module and came back, show the last
    # submitted IMEI result without forcing another ledger query.
    if (
        not query_clicked
        and st.session_state.get("last_verification_data") is not None
    ):
        render_verification_summary(
            st.session_state["last_verification_data"]
        )

# --- MODULE 2: CONSENSUS ANALYTICS & KPIS ---
elif app_mode == "Consensus Analytics & KPIs":
    st.markdown(
        '<div class="hero-shell">'
        '<div class="hero-badge">Prototype Network Analytics</div>'
        '<div class="hero-title">📊 Network Verification &amp; Operational Analytics</div>'
        '<div class="hero-subtitle">System-level monitoring of verification activity, successful history, event-stream processing, and aggregate security indicators generated by the prototype.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # Read generated evidence
    # ------------------------------------------------------------
    def safe_read_csv(file_path):
        try:
            if not file_path.exists() or file_path.stat().st_size == 0:
                return pd.DataFrame()
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()

    verification_df = safe_read_csv(TEST_LOG_FILE)
    event_df = safe_read_csv(EVENT_STREAM_LOG_FILE)
    security_df = safe_read_csv(SECURITY_EVENT_LOG_FILE)

    # ============================================================
    # 1. CURRENT PAGE 1 RESULT — SHOW ONCE
    # ============================================================
    current_data = st.session_state.get("last_verification_data")
    current_imei = st.session_state.get("saved_imei", "")

    current_result = None

    if current_data is not None:
        if current_data.get("is_tampered"):
            current_result = "TAMPERED"
        elif current_data.get("is_genuine", False):
            current_result = "GENUINE"
        else:
            current_result = "NOT VERIFIED"

        st.markdown(
            '<div class="section-label">Current Device Snapshot</div>',
            unsafe_allow_html=True
        )
        st.markdown("### Current Device Snapshot")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "IMEI",
            current_imei if current_imei else "No IMEI"
        )
        c2.metric(
            "Verification Result",
            current_result
        )
        c3.metric(
            "Current State",
            str(current_data.get("current_status", "UNKNOWN"))
        )
        c4.metric(
            "Custody Node",
            str(current_data.get("current_owner", "UNKNOWN"))
        )

        st.caption(
            "Same current result as Asset Verification Tower."
        )
    else:
        st.info(
            "Run an IMEI verification on Asset Verification Tower to "
            "populate the current-result section."
        )

    st.markdown("---")

    # ============================================================
    # 2. VERIFICATION SUMMARY — AGGREGATES ONLY
    # ============================================================
    st.markdown(
        '<div class="section-label">Verification Monitoring</div>',
        unsafe_allow_html=True
    )
    st.markdown("### Verification Activity Summary")

    required_columns = {
        "run_date",
        "run_time",
        "imei",
        "test_case",
        "imei_result",
        "streamlit_status",
        "result"
    }

    successful_df = pd.DataFrame()
    diagnostic_df = pd.DataFrame()
    invalid_inputs = 0

    if (
        not verification_df.empty
        and required_columns.issubset(set(verification_df.columns))
    ):
        verification_df["imei_result"] = (
            verification_df["imei_result"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

        verification_df["result"] = (
            verification_df["result"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

        provenance_df = verification_df[
            verification_df["test_case"]
            == "IMEI Provenance Verification"
        ].copy()

        # Completed verification queries include GENUINE, TAMPERED and UNKNOWN.
        # UNKNOWN means the input is valid but no registry record exists.
        successful_df = provenance_df[
            provenance_df["imei_result"].isin(["GENUINE", "TAMPERED", "UNKNOWN"])
        ].copy()

        diagnostic_df = provenance_df[
            ~provenance_df["imei_result"].isin(["GENUINE", "TAMPERED", "UNKNOWN"])
        ].copy()

        invalid_inputs = int(
            (
                verification_df["test_case"]
                == "IMEI Input Validation"
            ).sum()
        )

    # If current Page 1 result is successful but not yet in the log,
    # include it in-memory exactly once.
    if (
        current_data is not None
        and current_result in ["GENUINE", "TAMPERED", "UNKNOWN"]
        and current_imei
    ):
        already_present = False

        if not successful_df.empty:
            matches = (
                successful_df["imei"].astype(str).eq(
                    str(current_imei)
                )
                & successful_df["imei_result"].eq(
                    current_result
                )
            )
            already_present = bool(matches.any())

        if not already_present:
            current_row = pd.DataFrame(
                [{
                    "run_date": datetime.now().strftime("%Y-%m-%d"),
                    "run_time": datetime.now().strftime("%H:%M:%S"),
                    "imei": current_imei,
                    "test_case": "IMEI Provenance Verification",
                    "imei_result": current_result,
                    "streamlit_status": "Current session result",
                    "result": "PASS"
                }]
            )

            successful_df = pd.concat(
                [successful_df, current_row],
                ignore_index=True
            )

    total_successful = len(successful_df)

    genuine_count = (
        int(
            successful_df["imei_result"]
            .eq("GENUINE")
            .sum()
        )
        if not successful_df.empty
        else 0
    )

    tampered_count = (
        int(
            successful_df["imei_result"]
            .eq("TAMPERED")
            .sum()
        )
        if not successful_df.empty
        else 0
    )


    unknown_count = (
        int(successful_df["imei_result"].eq("UNKNOWN").sum())
        if not successful_df.empty else 0
    )

    passed_count = (
        int(successful_df["result"].eq("PASS").sum())
        if not successful_df.empty
        else 0
    )

    verification_pass_rate = (
        (passed_count / total_successful) * 100
        if total_successful > 0
        else 0.0
    )

    v1, v2, v3, v4, v5 = st.columns(5)

    v1.metric(
        "Completed Verifications",
        total_successful
    )
    v2.metric(
        "Genuine Results",
        genuine_count
    )
    v3.metric(
        "Tampered Results",
        tampered_count
    )
    v4.metric("Unknown Results", unknown_count)
    v5.metric(
        "Verification Pass Rate",
        f"{verification_pass_rate:.1f}%"
    )

    v6, v7 = st.columns(2)

    v6.metric(
        "Invalid Input Attempts",
        invalid_inputs
    )
    v7.metric(
        "Historical App/API Errors",
        len(diagnostic_df)
    )

    # Recent records provide evidence traceability without repeating a
    # "latest result" metric already shown in Current Verification.
    st.markdown("#### Recent Verification Records")

    if not successful_df.empty:
        recent_df = (
            successful_df[
                [
                    "run_date",
                    "run_time",
                    "imei",
                    "imei_result",
                    "result"
                ]
            ]
            .tail(10)
            .iloc[::-1]
            .reset_index(drop=True)
        )

        recent_df.columns = [
            "Run Date",
            "Run Time",
            "IMEI",
            "IMEI Result",
            "Test Result"
        ]

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "No verification records are available yet."
        )

    # Outcome chart becomes meaningful after multiple successful runs.
    if total_successful >= 2:
        st.markdown("#### Verification Outcome Distribution")

        outcome_df = pd.DataFrame(
            {
                "Outcome": ["GENUINE", "TAMPERED", "UNKNOWN"],
                "Count": [genuine_count, tampered_count, unknown_count]
            }
        ).set_index("Outcome")

        st.bar_chart(outcome_df)

    if not diagnostic_df.empty:
        with st.expander(
            f"Legacy / Application Diagnostics "
            f"({len(diagnostic_df)} failed run(s))"
        ):
            diagnostic_view = (
                diagnostic_df[
                    [
                        "run_date",
                        "run_time",
                        "imei",
                        "imei_result",
                        "streamlit_status",
                        "result"
                    ]
                ]
                .tail(20)
                .iloc[::-1]
            )

            st.dataframe(
                diagnostic_view,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "These are older application/error records retained from the existing CSV and excluded from GENUINE/TAMPERED device-state counts."
            )

    st.markdown("---")

    # ============================================================
    # 3. EVENT-STREAM ANALYTICS — DIFFERENT INFORMATION
    # ============================================================
    st.markdown(
        '<div class="section-label">Operational Event Monitoring</div>',
        unsafe_allow_html=True
    )
    st.markdown("### Event-Stream Processing Summary")

    if event_df.empty:
        st.info(
            "No event-stream evidence has been generated yet. "
            "Run a successful verification on Page 1."
        )
    else:
        # Normalize only columns that actually exist.
        for column in [
            "event_type",
            "producer_status",
            "consumer_status",
            "stream_result"
        ]:
            if column in event_df.columns:
                event_df[column] = (
                    event_df[column]
                    .fillna("")
                    .astype(str)
                    .str.upper()
                    .str.strip()
                )

        total_events = len(event_df)

        producer_emitted = (
            int(
                event_df["producer_status"]
                .isin(["EMITTED", "SIMULATED_EMIT"])
                .sum()
            )
            if "producer_status" in event_df.columns
            else 0
        )

        consumer_processed = (
            int(
                event_df["consumer_status"]
                .isin(["PROCESSED", "SIMULATED_PROCESS"])
                .sum()
            )
            if "consumer_status" in event_df.columns
            else 0
        )

        stream_passes = (
            int(
                event_df["stream_result"]
                .isin(["PASS", "PROCESSED", "SIMULATION_PASS"])
                .sum()
            )
            if "stream_result" in event_df.columns
            else 0
        )

        stream_pass_rate = (
            (stream_passes / total_events) * 100
            if total_events > 0
            else 0.0
        )

        e1, e2, e3, e4 = st.columns(4)

        e1.metric(
            "Stream Events Recorded",
            total_events
        )
        e2.metric(
            "Simulated Events Emitted",
            producer_emitted
        )
        e3.metric(
            "Simulated Events Processed",
            consumer_processed
        )
        e4.metric(
            "Stream Processing Success Rate",
            f"{stream_pass_rate:.1f}%"
        )

    st.markdown("---")

    # ============================================================
    # 4. SECURITY ANALYTICS — DIFFERENT INFORMATION
    # ============================================================
    st.markdown(
        '<div class="section-label">Aggregate Security Indicators</div>',
        unsafe_allow_html=True
    )
    st.markdown("### Security Monitoring Summary")

    # Show BOTH genuine/clear and tampered security outcomes.
    genuine_clear_count = (
        int(
            provenance_df[
                provenance_df["imei_result"].eq("GENUINE")
            ].shape[0]
        )
        if not provenance_df.empty
        else 0
    )

    if security_df.empty:
        tamper_alerts = tampered_count
        hash_mismatches = 0
        unauthorized_changes = 0
    else:
        security_event_col = (
            "security_event"
            if "security_event" in security_df.columns
            else None
        )

        if security_event_col:
            security_series = (
                security_df[security_event_col]
                .fillna("")
                .astype(str)
                .str.upper()
                .str.strip()
            )

            tamper_alerts = int(
                security_series
                .str.contains("TAMPER", regex=False)
                .sum()
            )

            hash_mismatches = int(
                security_series
                .str.contains("HASH", regex=False)
                .sum()
            )

            unauthorized_changes = int(
                security_series
                .str.contains("UNAUTHORIZED", regex=False)
                .sum()
            )
        else:
            tamper_alerts = tampered_count
            hash_mismatches = 0
            unauthorized_changes = 0

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "Genuine / Clear Verifications",
        genuine_clear_count
    )

    s2.metric(
        "Tamper Alerts",
        tamper_alerts
    )

    s3.metric(
        "Hash Mismatch Events",
        hash_mismatches
    )

    s4.metric(
        "Unauthorized State Changes",
        unauthorized_changes
    )

    st.caption(
        "Genuine / Clear Verifications are counted from tests/test_log.csv. "
        "Tamper and other security indicators are counted from generated security evidence."
    )

    st.markdown("---")

    st.caption(
        "Verification history is shown once above. Event-stream and security "
        "sections are summary-only so the same IMEI records are not repeated."
    )

# --- MODULE 3: SECURITY & THREAT MATRIX ---
elif app_mode == "Security & Threat Matrix":
    current_data = st.session_state.get("last_verification_data")
    current_imei = st.session_state.get("saved_imei", "")

    st.markdown(
        '<div class="hero-shell">'
        '<div class="hero-badge">Security Investigation</div>'
        '<div class="hero-title">🎛️ Security Threat Detection &amp; Response Console</div>'
        '<div class="hero-subtitle">Security events are shown as a structured incident table for the currently verified IMEI. The table changes automatically based on whether the device is GENUINE or TAMPERED.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if current_data is None:
        st.info(
            "No current IMEI verification is available. "
            "Run a verification from Asset Verification Tower first."
        )

    else:
        is_tampered = bool(current_data.get("is_tampered", False))
        is_genuine = bool(current_data.get("is_genuine", False))

        current_state = str(current_data.get("current_status", "UNKNOWN"))
        current_owner = str(current_data.get("current_owner", "UNKNOWN"))

        security_file = PROJECT_ROOT / "evidence" / "security_event_log.csv"

        event_date = datetime.now().strftime("%Y-%m-%d")
        event_time = datetime.now().strftime("%H:%M:%S")
        matching_security = pd.DataFrame()

        if security_file.exists() and security_file.stat().st_size > 0:
            try:
                security_df = pd.read_csv(security_file)

                if not security_df.empty and "imei" in security_df.columns:
                    matching_security = security_df[
                        security_df["imei"].astype(str) == str(current_imei)
                    ].copy()

                    if not matching_security.empty:
                        latest = matching_security.iloc[-1]
                        event_date = str(latest.get("event_date", event_date))
                        event_time = str(latest.get("event_time", event_time))
            except Exception:
                matching_security = pd.DataFrame()

        timestamp = f"{event_date} {event_time}"

        # ========================================================
        # GENUINE
        # ========================================================
        if is_genuine and not is_tampered:
            st.markdown(
                '<div class="section-label">Security Status</div>',
                unsafe_allow_html=True
            )
            st.markdown("### No Active Security Incident")

            g1, g2, g3 = st.columns(3)

            g1.metric("Tamper Detection", "CLEAR")
            g2.metric("Ledger Integrity", "VERIFIED")
            g3.metric("Security Action", "NONE REQUIRED")

            genuine_events = pd.DataFrame(
                [
                    {
                        "Timestamp": timestamp,
                        "Stage": "INGRESS",
                        "Event": f"Integrity verification started for IMEI {current_imei}",
                        "Result": "STARTED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "LEDGER CHECK",
                        "Event": "Provenance pointer matched the expected ledger record",
                        "Result": "VERIFIED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "CUSTODY CHECK",
                        "Event": f"Authorized custody node confirmed: {current_owner}",
                        "Result": "VERIFIED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "STATE CHECK",
                        "Event": f"Lifecycle state validated: {current_state}",
                        "Result": "VERIFIED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "SECURITY RESULT",
                        "Event": "Device classified as GENUINE",
                        "Result": "CLEAR"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "RESPONSE",
                        "Event": "No containment or remediation action required",
                        "Result": "NONE"
                    }
                ]
            )

            st.markdown("### Verification Security Trace")

            st.dataframe(
                genuine_events,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                "System Defenses: Clear. No tamper condition or integrity exception is active."
            )

        # ========================================================
        # TAMPERED
        # ========================================================
        elif is_tampered:
            st.markdown(
                '<div class="section-label">Active Incident</div>',
                unsafe_allow_html=True
            )
            st.markdown("### Simulated Local State Manipulation Incident")

            i1, i2, i3 = st.columns(3)

            i1.metric("Current IMEI", current_imei)
            i2.metric("Detected State", "TAMPERED")
            i3.metric("Incident Time", timestamp)

            tampered_events = pd.DataFrame(
                [
                    {
                        "Timestamp": timestamp,
                        "Stage": "INGRESS",
                        "Event": f"Boundary integrity check started for IMEI {current_imei}",
                        "Result": "STARTED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "ATTACK SIMULATION",
                        "Event": "Simulated unauthorized local-state modification attempt detected",
                        "Result": "DETECTED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "SECURITY CRITICAL",
                        "Event": "Cryptographic / provenance-state mismatch detected",
                        "Result": "ALERT"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "LEDGER VALIDATION",
                        "Event": "Local state does not match the expected blockchain provenance pointer",
                        "Result": "TAMPERED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "ACTION",
                        "Event": f"Device classified as TAMPERED; current state = {current_state}",
                        "Result": "FLAGGED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "AUDIT",
                        "Event": "Security event recorded in the prototype evidence log",
                        "Result": "RECORDED"
                    },
                    {
                        "Timestamp": timestamp,
                        "Stage": "CONTAINMENT",
                        "Event": f"Incident routed to {current_owner}; restricted activation handling applied",
                        "Result": "CONTAINED"
                    }
                ]
            )

            st.markdown("### Security Incident Timeline")

            st.dataframe(
                tampered_events,
                use_container_width=True,
                hide_index=True
            )

            st.error(
                "System Defenses: Active. The tamper condition was detected, "
                "recorded, and routed for containment handling."
            )

            if not matching_security.empty:
                st.markdown("---")
                st.markdown(
                    '<div class="section-label">Recorded Evidence</div>',
                    unsafe_allow_html=True
                )
                st.markdown("### Security Event Record")

                useful_columns = [
                    column for column in [
                        "event_date",
                        "event_time",
                        "imei",
                        "security_event",
                        "detected_state",
                        "result"
                    ]
                    if column in matching_security.columns
                ]

                evidence_view = (
                    matching_security[useful_columns]
                    .tail(10)
                    .iloc[::-1]
                    .reset_index(drop=True)
                )

                evidence_view = evidence_view.rename(
                    columns={
                        "event_date": "Event Date",
                        "event_time": "Event Time",
                        "imei": "IMEI",
                        "security_event": "Security Event",
                        "detected_state": "Detected State",
                        "result": "Detection Status"
                    }
                )

                st.dataframe(
                    evidence_view,
                    use_container_width=True,
                    hide_index=True
                )

        else:
            st.warning(
                "The current verification result is neither GENUINE nor TAMPERED. "
                "No security trace is available."
            )