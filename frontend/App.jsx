// ============================================================
// ChurnIQ Customer Intelligence - Refined SaaS React App
// ============================================================

const { useState, useEffect, useRef } = React;

function App() {
    const [activePage, setActivePage] = useState("dashboard");
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [theme, setTheme] = useState("dark");
    const [apiConnected, setApiConnected] = useState(true);
    
    // Prediction Form State
    const [formData, setFormData] = useState({
        gender: "Female",
        SeniorCitizen: 0,
        Partner: "No",
        Dependents: "No",
        tenure: 1,
        PhoneService: "Yes",
        MultipleLines: "No",
        InternetService: "Fiber optic",
        OnlineSecurity: "No",
        OnlineBackup: "No",
        DeviceProtection: "No",
        TechSupport: "No",
        StreamingTV: "No",
        StreamingMovies: "No",
        Contract: "Month-to-month",
        PaperlessBilling: "Yes",
        PaymentMethod: "Electronic check",
        MonthlyCharges: 70.35,
        TotalCharges: 70.35
    });

    const [predicting, setPredicting] = useState(false);
    const [predictionResult, setPredictionResult] = useState(null);
    const [predictError, setPredictError] = useState(null);

    // Prediction History (stored in localStorage)
    const [history, setHistory] = useState(() => {
        try {
            const saved = localStorage.getItem("churniq_history");
            return saved ? JSON.parse(saved) : [];
        } catch {
            return [];
        }
    });

    // Check API Health Status on mount
    useEffect(() => {
        checkApiHealth();
    }, []);

    const checkApiHealth = async () => {
        try {
            const res = await fetch("https://churniq-api-cds0.onrender.com/health");
            if (res.ok) setApiConnected(true);
            else setApiConnected(false);
        } catch {
            setApiConnected(false);
        }
    };

    // Save history to localStorage
    useEffect(() => {
        try {
            localStorage.setItem("churniq_history", JSON.stringify(history));
        } catch (e) {
            console.error("Failed saving history to localStorage", e);
        }
    }, [history]);

    // Handle Form Change
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        let parsed = value;
        if (name === "SeniorCitizen" || name === "tenure") {
            parsed = parseInt(value) || 0;
        } else if (name === "MonthlyCharges" || name === "TotalCharges") {
            parsed = parseFloat(value) || 0;
        }
        setFormData(prev => ({ ...prev, [name]: parsed }));
    };

    // Preset Sample Loaders
    const loadSampleProfile = (type) => {
        if (type === "high_risk") {
            setFormData({
                gender: "Female",
                SeniorCitizen: 0,
                Partner: "No",
                Dependents: "No",
                tenure: 2,
                PhoneService: "Yes",
                MultipleLines: "No",
                InternetService: "Fiber optic",
                OnlineSecurity: "No",
                OnlineBackup: "No",
                DeviceProtection: "No",
                TechSupport: "No",
                StreamingTV: "Yes",
                StreamingMovies: "Yes",
                Contract: "Month-to-month",
                PaperlessBilling: "Yes",
                PaymentMethod: "Electronic check",
                MonthlyCharges: 95.75,
                TotalCharges: 191.50
            });
        } else if (type === "low_risk") {
            setFormData({
                gender: "Male",
                SeniorCitizen: 0,
                Partner: "Yes",
                Dependents: "Yes",
                tenure: 72,
                PhoneService: "Yes",
                MultipleLines: "Yes",
                InternetService: "DSL",
                OnlineSecurity: "Yes",
                OnlineBackup: "Yes",
                DeviceProtection: "Yes",
                TechSupport: "Yes",
                StreamingTV: "Yes",
                StreamingMovies: "Yes",
                Contract: "Two year",
                PaperlessBilling: "No",
                PaymentMethod: "Credit card (automatic)",
                MonthlyCharges: 85.00,
                TotalCharges: 6120.00
            });
        }
    };

    // Handle Prediction Submission
    const handlePredictSubmit = async (e) => {
        e.preventDefault();
        setPredicting(true);
        setPredictError(null);
        setPredictionResult(null);

        try {
            const response = await fetch("https://churniq-api-cds0.onrender.com/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error("FastAPI server returned error status " + response.status);
            }

            const data = await response.json();
            setPredictionResult(data);

            // Add to prediction history
            const newHistoryItem = {
                id: "PRD-" + Math.floor(1000 + Math.random() * 9000),
                timestamp: new Date().toLocaleTimeString() + ", " + new Date().toLocaleDateString(),
                contract: formData.Contract,
                tenure: formData.tenure,
                monthlyCharges: formData.MonthlyCharges,
                prediction: data.prediction,
                probability: data.churn_probability,
                risk: data.risk_level
            };

            setHistory(prev => [newHistoryItem, ...prev]);
        } catch (err) {
            setPredictError(err.message + " - Ensure FastAPI server is running at https://churniq-api-cds0.onrender.com");
        } finally {
            setPredicting(false);
        }
    };

    // Theme Toggle Effect
    const toggleTheme = () => {
        const next = theme === "dark" ? "light" : "dark";
        setTheme(next);
        document.documentElement.setAttribute("data-theme", next);
    };

    return (
        <div className="app-container">
            {/* --- Persistent Sidebar Navigation --- */}
            <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
                <div className="sidebar-brand">
                    <div className="brand-icon">⚡</div>
                    <div>
                        <span className="brand-title">ChurnIQ</span>
                        <span className="brand-subtitle">Customer Intelligence</span>
                    </div>
                </div>

                <div className="sidebar-menu">
                    <div className="menu-category">Analytics & Workspace</div>
                    <div className={`menu-item ${activePage === "dashboard" ? "active" : ""}`} onClick={() => setActivePage("dashboard")}>
                        <i className="fa-solid fa-chart-pie"></i> Dashboard
                    </div>
                    <div className={`menu-item ${activePage === "predict" ? "active" : ""}`} onClick={() => setActivePage("predict")}>
                        <i className="fa-solid fa-bullseye"></i> Predict Churn
                    </div>
                    <div className={`menu-item ${activePage === "customers" ? "active" : ""}`} onClick={() => setActivePage("customers")}>
                        <i className="fa-solid fa-users"></i> Customers
                    </div>
                    <div className={`menu-item ${activePage === "analytics" ? "active" : ""}`} onClick={() => setActivePage("analytics")}>
                        <i className="fa-solid fa-chart-column"></i> Analytics
                    </div>
                    <div className={`menu-item ${activePage === "history" ? "active" : ""}`} onClick={() => setActivePage("history")}>
                        <i className="fa-solid fa-clock-rotate-left"></i> Prediction History
                    </div>
                    <div className={`menu-item ${activePage === "insights" ? "active" : ""}`} onClick={() => setActivePage("insights")}>
                        <i className="fa-solid fa-brain"></i> Model Insights
                    </div>

                    <div className="menu-category" style={{ marginTop: "1rem" }}>System</div>
                    <div className={`menu-item ${activePage === "about" ? "active" : ""}`} onClick={() => setActivePage("about")}>
                        <i className="fa-solid fa-circle-info"></i> About & Docs
                    </div>
                    <div className={`menu-item ${activePage === "settings" ? "active" : ""}`} onClick={() => setActivePage("settings")}>
                        <i className="fa-solid fa-gear"></i> Settings
                    </div>
                </div>

                <div className="sidebar-footer">
                    <div className="api-status-badge">
                        <div className={`status-dot ${apiConnected ? "" : "disconnected"}`}></div>
                        <span>{apiConnected ? "API Connected" : "API Offline"}</span>
                    </div>
                </div>
            </aside>

            {/* --- Main Content Wrapper --- */}
            <main className="main-wrapper">
                {/* --- Top Header Bar --- */}
                <header className="top-header">
                    <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                        <button className="btn-secondary-saas" style={{ padding: "0.4rem 0.75rem", display: "none" }} onClick={() => setSidebarOpen(!sidebarOpen)}>
                            <i className="fa-solid fa-bars"></i>
                        </button>
                        <h2 className="page-title">
                            {activePage === "dashboard" && <span><i className="fa-solid fa-chart-pie me-2 text-indigo"></i>Executive Churn Intelligence Dashboard</span>}
                            {activePage === "predict" && <span><i className="fa-solid fa-bullseye me-2 text-indigo"></i>Real-Time Churn Risk Assessment</span>}
                            {activePage === "customers" && <span><i className="fa-solid fa-users me-2 text-indigo"></i>Customer Directory & Risk Analysis</span>}
                            {activePage === "analytics" && <span><i className="fa-solid fa-chart-column me-2 text-indigo"></i>Behavioral Churn Analytics</span>}
                            {activePage === "history" && <span><i className="fa-solid fa-clock-rotate-left me-2 text-indigo"></i>Prediction Audit Log</span>}
                            {activePage === "insights" && <span><i className="fa-solid fa-brain me-2 text-indigo"></i>Model Performance & Explainability</span>}
                            {activePage === "about" && <span><i className="fa-solid fa-circle-info me-2 text-indigo"></i>Project Architecture & Docs</span>}
                            {activePage === "settings" && <span><i className="fa-solid fa-gear me-2 text-indigo"></i>System Settings</span>}
                        </h2>
                    </div>

                    <div className="header-actions">
                        <div className="model-pill">
                            <i className="fa-solid fa-shield-halved"></i> Random Forest (Tuned) • 81.3% Recall
                        </div>
                        <button className="btn-secondary-saas" onClick={toggleTheme} title="Toggle Dark/Light Theme">
                            <i className={theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon"}></i>
                        </button>
                    </div>
                </header>

                {/* --- Dynamic Page Render --- */}
                <div className="content-body">
                    {activePage === "dashboard" && <DashboardPage history={history} onPredictClick={() => setActivePage("predict")} />}
                    {activePage === "predict" && (
                        <PredictPage
                            formData={formData}
                            handleInputChange={handleInputChange}
                            handlePredictSubmit={handlePredictSubmit}
                            predicting={predicting}
                            predictionResult={predictionResult}
                            predictError={predictError}
                            loadSampleProfile={loadSampleProfile}
                            setActivePage={setActivePage}
                        />
                    )}
                    {activePage === "customers" && <CustomersPage />}
                    {activePage === "analytics" && <AnalyticsPage />}
                    {activePage === "history" && <HistoryPage history={history} setHistory={setHistory} />}
                    {activePage === "insights" && <InsightsPage />}
                    {activePage === "about" && <AboutPage />}
                    {activePage === "settings" && <SettingsPage apiConnected={apiConnected} checkApiHealth={checkApiHealth} theme={theme} toggleTheme={toggleTheme} />}
                </div>
            </main>
        </div>
    );
}

// ============================================================
// PAGE 1: REFINED DASHBOARD PAGE
// ============================================================
function DashboardPage({ history, onPredictClick }) {
    const chart1Ref = useRef(null);
    const chart2Ref = useRef(null);
    const chart1Instance = useRef(null);
    const chart2Instance = useRef(null);

    // Calculate live session high-risk count
    const liveHighRiskCount = history.filter(h => h.risk === "High Risk").length;

    useEffect(() => {
        if (chart1Ref.current) {
            if (chart1Instance.current) chart1Instance.current.destroy();
            chart1Instance.current = new Chart(chart1Ref.current, {
                type: 'doughnut',
                data: {
                    labels: ['Historical Retained (73.5%)', 'Historical Churned (26.5%)'],
                    datasets: [{
                        data: [5174, 1869],
                        backgroundColor: ['#10b981', '#ef4444'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
                }
            });
        }

        if (chart2Ref.current) {
            if (chart2Instance.current) chart2Instance.current.destroy();
            chart2Instance.current = new Chart(chart2Ref.current, {
                type: 'bar',
                data: {
                    labels: ['Month-to-month', 'One year', 'Two year'],
                    datasets: [
                        { label: 'Retained', data: [2220, 1307, 1647], backgroundColor: '#10b981' },
                        { label: 'Churned', data: [1655, 166, 48], backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    },
                    plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
                }
            });
        }
    }, []);

    return (
        <div>
            {/* KPI Overview Grid */}
            <div className="kpi-grid">
                <div className="card-panel kpi-card" title="Total raw customer records in the Telco dataset (100%)">
                    <div className="kpi-icon indigo"><i className="fa-solid fa-users"></i></div>
                    <div>
                        <div className="kpi-val">7,043</div>
                        <div className="kpi-lbl">Total Dataset Customers</div>
                    </div>
                </div>

                <div className="card-panel kpi-card" title="Actual historical ground-truth churners in the dataset (26.54% churn rate)">
                    <div className="kpi-icon red"><i className="fa-solid fa-user-xmark"></i></div>
                    <div>
                        <div className="kpi-val">1,869</div>
                        <div className="kpi-lbl">Historical Churn Count <small style={{ color: "#ef4444" }}>(26.5%)</small></div>
                    </div>
                </div>

                <div className="card-panel kpi-card" title="High-Risk customer predictions generated during current live browser session">
                    <div className="kpi-icon amber"><i className="fa-solid fa-triangle-exclamation"></i></div>
                    <div>
                        <div className="kpi-val">{liveHighRiskCount}</div>
                        <div className="kpi-lbl">Session High-Risk Predictions</div>
                    </div>
                </div>

                <div className="card-panel kpi-card" title="Verified model test recall: percentage of actual churners correctly caught by the tuned Random Forest model">
                    <div className="kpi-icon green"><i className="fa-solid fa-shield-check"></i></div>
                    <div>
                        <div className="kpi-val">81.28%</div>
                        <div className="kpi-lbl">Model Test Recall Rate</div>
                    </div>
                </div>
            </div>

            {/* Model Evaluation & Confusion Matrix Section */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))", gap: "1.5rem", marginBottom: "2rem" }}>
                {/* Empirical Model Performance Metrics */}
                <div className="card-panel">
                    <h3 className="form-section-title">
                        <i className="fa-solid fa-square-poll-vertical me-2 text-indigo"></i>Holdout Test Model Evaluation Metrics
                    </h3>
                    <p style={{ color: "var(--text-secondary)", fontSize: "0.825rem", marginBottom: "1rem" }}>
                        Evaluated on <strong>1,407 unseen holdout test samples</strong> (`X_test`) after 5-fold cross-validation hyperparameter tuning.
                    </p>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.85rem" }}>
                        <div style={{ background: "rgba(15,23,42,0.6)", padding: "0.85rem", borderRadius: "8px", border: "1px solid var(--border-color)" }} title="Recall: Proportion of actual churners correctly caught">
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>RECALL (CHURN)</div>
                            <div style={{ fontSize: "1.4rem", fontWeight: 800, color: "var(--risk-low)" }}>81.28%</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>304 / 374 Churners Caught</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.6)", padding: "0.85rem", borderRadius: "8px", border: "1px solid var(--border-color)" }} title="ROC-AUC: Area under Receiver Operating Characteristic Curve">
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>ROC-AUC SCORE</div>
                            <div style={{ fontSize: "1.4rem", fontWeight: 800, color: "var(--accent-primary)" }}>0.8383</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>High Class Separation</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.6)", padding: "0.85rem", borderRadius: "8px", border: "1px solid var(--border-color)" }} title="Accuracy: Total correct predictions over test set">
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>ACCURACY</div>
                            <div style={{ fontSize: "1.4rem", fontWeight: 800, color: "var(--text-primary)" }}>73.99%</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>1,041 / 1,407 Correct</div>
                        </div>

                        <div style={{ background: "rgba(15,23,42,0.6)", padding: "0.85rem", borderRadius: "8px", border: "1px solid var(--border-color)" }} title="Precision: Proportion of predicted churners who actually churned">
                            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>PRECISION</div>
                            <div style={{ fontSize: "1.4rem", fontWeight: 800, color: "var(--risk-medium)" }}>50.67%</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>F1-Score: 0.6242</div>
                        </div>
                    </div>
                </div>

                {/* Confusion Matrix Widget */}
                <div className="card-panel">
                    <h3 className="form-section-title">
                        <i className="fa-solid fa-table-cells me-2 text-indigo"></i>Holdout Test Confusion Matrix
                    </h3>
                    <p style={{ color: "var(--text-secondary)", fontSize: "0.825rem", marginBottom: "1rem" }}>
                        Breakdown of model predictions vs actual ground truth on 1,407 test samples.
                    </p>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem", textAlign: "center" }}>
                        <div style={{ background: "rgba(16, 185, 129, 0.12)", border: "1px solid rgba(16, 185, 129, 0.3)", padding: "1rem", borderRadius: "8px" }} title="True Negatives: Retained customers correctly predicted as Retained">
                            <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--risk-low)" }}>TRUE NEGATIVES (TN)</div>
                            <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--text-primary)" }}>737</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>Retained $\rightarrow$ Retained</div>
                        </div>

                        <div style={{ background: "rgba(245, 158, 11, 0.12)", border: "1px solid rgba(245, 158, 11, 0.3)", padding: "1rem", borderRadius: "8px" }} title="False Positives: Retained customers predicted as Churners">
                            <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--risk-medium)" }}>FALSE POSITIVES (FP)</div>
                            <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--text-primary)" }}>296</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>Retained $\rightarrow$ Churn</div>
                        </div>

                        <div style={{ background: "rgba(239, 68, 68, 0.12)", border: "1px solid rgba(239, 68, 68, 0.3)", padding: "1rem", borderRadius: "8px" }} title="False Negatives: Missed churners predicted as Retained">
                            <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--risk-high)" }}>FALSE NEGATIVES (FN)</div>
                            <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--text-primary)" }}>70</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>Missed Churners</div>
                        </div>

                        <div style={{ background: "rgba(16, 185, 129, 0.2)", border: "1px solid rgba(16, 185, 129, 0.5)", padding: "1rem", borderRadius: "8px" }} title="True Positives: Churned customers correctly caught by the model">
                            <div style={{ fontSize: "0.75rem", fontWeight: 700, color: "var(--risk-low)" }}>TRUE POSITIVES (TP)</div>
                            <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--text-primary)" }}>304</div>
                            <div style={{ fontSize: "0.7rem", color: "var(--text-secondary)" }}>Caught Churners 🏆</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Analytics Charts Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))", gap: "1.5rem", marginBottom: "2rem" }}>
                <div className="card-panel">
                    <h3 className="form-section-title"><i className="fa-solid fa-chart-pie me-2 text-indigo"></i>Historical Churn Ratio</h3>
                    <div style={{ height: "240px" }}><canvas ref={chart1Ref}></canvas></div>
                </div>
                <div className="card-panel">
                    <h3 className="form-section-title"><i className="fa-solid fa-chart-bar me-2 text-indigo"></i>Churn Breakdown by Contract</h3>
                    <div style={{ height: "240px" }}><canvas ref={chart2Ref}></canvas></div>
                </div>
            </div>

            {/* Recent Predictions Audit */}
            <div className="card-panel">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
                    <h3 className="form-section-title" style={{ border: "none", margin: 0, padding: 0 }}>
                        <i className="fa-solid fa-clock-rotate-left me-2 text-indigo"></i>Recent Session Live Predictions
                    </h3>
                    <button className="btn-primary-saas" onClick={onPredictClick}>
                        <i className="fa-solid fa-plus me-1"></i> New Risk Assessment
                    </button>
                </div>

                <div className="table-responsive">
                    <table className="saas-table">
                        <thead>
                            <tr>
                                <th>Prediction ID</th>
                                <th>Timestamp</th>
                                <th>Contract Type</th>
                                <th>Tenure</th>
                                <th>Monthly Spend</th>
                                <th>Probability</th>
                                <th>Risk Category</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.length === 0 ? (
                                <tr>
                                    <td colSpan="7" style={{ textAlign: "center", padding: "2rem", color: "#94a3b8" }}>
                                        No recent predictions made yet in this browser session. Click <strong>New Risk Assessment</strong> to test the model.
                                    </td>
                                </tr>
                            ) : (
                                history.slice(0, 5).map(item => (
                                    <tr key={item.id}>
                                        <td style={{ fontWeight: 600 }}>{item.id}</td>
                                        <td>{item.timestamp}</td>
                                        <td>{item.contract}</td>
                                        <td>{item.tenure} mos</td>
                                        <td>${item.monthlyCharges.toFixed(2)}</td>
                                        <td style={{ fontWeight: 700 }}>{(item.probability * 100).toFixed(1)}%</td>
                                        <td>
                                            <span className={`badge-risk ${item.risk === 'High Risk' ? 'high' : item.risk === 'Medium Risk' ? 'medium' : 'low'}`}>
                                                {item.risk}
                                            </span>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 2: PREDICT CHURN PAGE
// ============================================================
function PredictPage({ formData, handleInputChange, handlePredictSubmit, predicting, predictionResult, predictError, loadSampleProfile, setActivePage }) {
    return (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))", gap: "1.5rem" }}>
            {/* Input Form Panel */}
            <div className="card-panel">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem" }}>
                    <h3 className="form-section-title" style={{ border: "none", margin: 0, padding: 0 }}>
                        <i className="fa-solid fa-user-gear me-2 text-indigo"></i>Customer Profile Workspace
                    </h3>
                    <div style={{ display: "flex", gap: "0.5rem" }}>
                        <button type="button" className="btn-secondary-saas" style={{ fontSize: "0.75rem", padding: "0.35rem 0.65rem" }} onClick={() => loadSampleProfile("high_risk")}>
                            🔴 Sample High-Risk
                        </button>
                        <button type="button" className="btn-secondary-saas" style={{ fontSize: "0.75rem", padding: "0.35rem 0.65rem" }} onClick={() => loadSampleProfile("low_risk")}>
                            🟢 Sample Low-Risk
                        </button>
                    </div>
                </div>

                <form onSubmit={handlePredictSubmit}>
                    {/* Section 1: Demographics */}
                    <div className="form-section-title"><i className="fa-solid fa-id-card"></i> 1. Customer Demographics</div>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "1rem" }}>
                        <div className="form-group">
                            <label className="form-label">Gender</label>
                            <select className="form-select" name="gender" value={formData.gender} onChange={handleInputChange}>
                                <option value="Female">Female</option>
                                <option value="Male">Male</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Senior Citizen</label>
                            <select className="form-select" name="SeniorCitizen" value={formData.SeniorCitizen} onChange={handleInputChange}>
                                <option value={0}>No (0)</option>
                                <option value={1}>Yes (1)</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Partner</label>
                            <select className="form-select" name="Partner" value={formData.Partner} onChange={handleInputChange}>
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Dependents</label>
                            <select className="form-select" name="Dependents" value={formData.Dependents} onChange={handleInputChange}>
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Tenure (Months): {formData.tenure}</label>
                            <input type="number" className="form-control" name="tenure" value={formData.tenure} min="0" max="100" onChange={handleInputChange} required />
                        </div>
                    </div>

                    {/* Section 2: Services */}
                    <div className="form-section-title" style={{ marginTop: "1rem" }}><i className="fa-solid fa-wifi"></i> 2. Subscriptions & Services</div>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "1rem" }}>
                        <div className="form-group">
                            <label className="form-label">Internet Service</label>
                            <select className="form-select" name="InternetService" value={formData.InternetService} onChange={handleInputChange}>
                                <option value="Fiber optic">Fiber optic</option>
                                <option value="DSL">DSL</option>
                                <option value="No">No</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Online Security</label>
                            <select className="form-select" name="OnlineSecurity" value={formData.OnlineSecurity} onChange={handleInputChange}>
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                                <option value="No internet service">No internet service</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Tech Support</label>
                            <select className="form-select" name="TechSupport" value={formData.TechSupport} onChange={handleInputChange}>
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                                <option value="No internet service">No internet service</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Multiple Lines</label>
                            <select className="form-select" name="MultipleLines" value={formData.MultipleLines} onChange={handleInputChange}>
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                                <option value="No phone service">No phone service</option>
                            </select>
                        </div>
                    </div>

                    {/* Section 3: Billing */}
                    <div className="form-section-title" style={{ marginTop: "1rem" }}><i className="fa-solid fa-credit-card"></i> 3. Billing & Contract</div>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "1rem" }}>
                        <div className="form-group">
                            <label className="form-label">Contract Type</label>
                            <select className="form-select" name="Contract" value={formData.Contract} onChange={handleInputChange}>
                                <option value="Month-to-month">Month-to-month</option>
                                <option value="One year">One year</option>
                                <option value="Two year">Two year</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Payment Method</label>
                            <select className="form-select" name="PaymentMethod" value={formData.PaymentMethod} onChange={handleInputChange}>
                                <option value="Electronic check">Electronic check</option>
                                <option value="Mailed check">Mailed check</option>
                                <option value="Bank transfer (automatic)">Bank transfer (automatic)</option>
                                <option value="Credit card (automatic)">Credit card (automatic)</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label className="form-label">Monthly Charges ($)</label>
                            <input type="number" step="0.01" className="form-control" name="MonthlyCharges" value={formData.MonthlyCharges} onChange={handleInputChange} required />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Total Charges ($)</label>
                            <input type="number" step="0.01" className="form-control" name="TotalCharges" value={formData.TotalCharges} onChange={handleInputChange} required />
                        </div>
                    </div>

                    <div style={{ marginTop: "1.5rem", textAlign: "right" }}>
                        <button type="submit" className="btn-primary-saas" disabled={predicting}>
                            {predicting ? <><i className="fa-solid fa-spinner fa-spin"></i> Analyzing...</> : <><i className="fa-solid fa-bolt"></i> Analyze Customer Risk</>}
                        </button>
                    </div>
                </form>
            </div>

            {/* Results Panel */}
            <div className="card-panel result-gauge-card">
                <h3 className="form-section-title" style={{ justifyContent: "center" }}>
                    <i className="fa-solid fa-shield-cat me-2 text-indigo"></i>Risk Assessment Result
                </h3>

                {predictError && (
                    <div style={{ backgroundColor: "var(--risk-high-bg)", border: "1px solid var(--risk-high)", color: "var(--risk-high)", padding: "1rem", borderRadius: "8px", margin: "1rem 0", textAlign: "left" }}>
                        <i className="fa-solid fa-triangle-exclamation me-2"></i> {predictError}
                    </div>
                )}

                {!predictionResult && !predictError && (
                    <div style={{ padding: "4rem 1rem", color: "var(--text-muted)" }}>
                        <i className="fa-solid fa-microchip fa-3x mb-3" style={{ opacity: 0.5 }}></i>
                        <p>Configure customer parameters and click <strong>Analyze Customer Risk</strong> to trigger Random Forest model inference.</p>
                    </div>
                )}

                {predictionResult && (
                    <div>
                        <div className={`probability-circle ${predictionResult.risk_level === 'High Risk' ? 'high' : predictionResult.risk_level === 'Medium Risk' ? 'medium' : 'low'}`}>
                            <span className="prob-number">{(predictionResult.churn_probability * 100).toFixed(1)}%</span>
                            <span className="prob-label">Probability</span>
                        </div>

                        <div style={{ margin: "1rem 0" }}>
                            <span className={`badge-risk ${predictionResult.risk_level === 'High Risk' ? 'high' : predictionResult.risk_level === 'Medium Risk' ? 'medium' : 'low'}`} style={{ fontSize: "0.9rem", padding: "0.5rem 1rem" }}>
                                {predictionResult.risk_level}
                            </span>
                        </div>

                        <h4 style={{ fontWeight: 800, color: predictionResult.prediction === 'Yes' ? 'var(--risk-high)' : 'var(--risk-low)', margin: "0.5rem 0" }}>
                            {predictionResult.prediction === 'Yes' ? 'LIKELY TO CHURN' : 'LIKELY TO RETAIN'}
                        </h4>

                        {/* Model-Supported Feature Explanations */}
                        <div className="risk-factors-list">
                            <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--text-primary)", marginBottom: "0.75rem" }}>
                                <i className="fa-solid fa-magnifying-glass-chart me-1 text-indigo"></i> Key Contributing Risk Drivers:
                            </div>

                            {formData.Contract === "Month-to-month" && (
                                <div className="risk-factor-item">
                                    <i className="fa-solid fa-triangle-exclamation text-amber" style={{ marginTop: "2px" }}></i>
                                    <span><strong>Month-to-month contract</strong>: Top historical driver of churn risk.</span>
                                </div>
                            )}

                            {formData.tenure < 12 && (
                                <div className="risk-factor-item">
                                    <i className="fa-solid fa-triangle-exclamation text-amber" style={{ marginTop: "2px" }}></i>
                                    <span><strong>Short tenure ({formData.tenure} months)</strong>: Early subscription churn window.</span>
                                </div>
                            )}

                            {formData.InternetService === "Fiber optic" && formData.TechSupport === "No" && (
                                <div className="risk-factor-item">
                                    <i className="fa-solid fa-triangle-exclamation text-amber" style={{ marginTop: "2px" }}></i>
                                    <span><strong>Fiber Optic without Tech Support</strong>: High friction correlation factor.</span>
                                </div>
                            )}

                            {formData.PaymentMethod === "Electronic check" && (
                                <div className="risk-factor-item">
                                    <i className="fa-solid fa-triangle-exclamation text-amber" style={{ marginTop: "2px" }}></i>
                                    <span><strong>Electronic Check payment</strong>: Higher churn rate than automatic billing.</span>
                                </div>
                            )}

                            {formData.Contract === "Two year" && (
                                <div className="risk-factor-item">
                                    <i className="fa-solid fa-circle-check text-green" style={{ marginTop: "2px" }}></i>
                                    <span><strong>2-Year Contract</strong>: Strongest customer retention stabilizer.</span>
                                </div>
                            )}
                        </div>

                        <div style={{ display: "flex", gap: "0.5rem", marginTop: "1.5rem", justifyContent: "center" }}>
                            <button className="btn-secondary-saas" onClick={() => setActivePage("analytics")}>View Analytics</button>
                            <button className="btn-secondary-saas" onClick={() => setActivePage("insights")}>Model Insights</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

// ============================================================
// PAGE 3: CUSTOMERS PAGE
// ============================================================
function CustomersPage() {
    const [search, setSearch] = useState("");
    const [riskFilter, setRiskFilter] = useState("All");

    const sampleCustomers = [
        { id: "CUST-7043", tenure: 1, contract: "Month-to-month", charges: 29.85, total: 29.85, prob: 0.787, risk: "High Risk", status: "Churned" },
        { id: "CUST-7042", tenure: 72, contract: "Two year", charges: 105.65, total: 7542.20, prob: 0.082, risk: "Low Risk", status: "Retained" },
        { id: "CUST-7041", tenure: 12, contract: "Month-to-month", charges: 84.80, total: 1018.60, prob: 0.621, risk: "Medium Risk", status: "Churned" },
        { id: "CUST-7040", tenure: 48, contract: "One year", charges: 55.20, total: 2649.60, prob: 0.154, risk: "Low Risk", status: "Retained" },
        { id: "CUST-7039", tenure: 3, contract: "Month-to-month", charges: 99.15, total: 297.45, prob: 0.814, risk: "High Risk", status: "Churned" },
        { id: "CUST-7038", tenure: 24, contract: "One year", charges: 64.70, total: 1552.80, prob: 0.312, risk: "Low Risk", status: "Retained" }
    ];

    const filtered = sampleCustomers.filter(c => {
        const matchesSearch = c.id.toLowerCase().includes(search.toLowerCase()) || c.contract.toLowerCase().includes(search.toLowerCase());
        const matchesRisk = riskFilter === "All" || c.risk === riskFilter;
        return matchesSearch && matchesRisk;
    });

    return (
        <div className="card-panel">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem", marginBottom: "1.5rem" }}>
                <div style={{ display: "flex", gap: "1rem", flex: 1, maxWidth: "500px" }}>
                    <input type="text" className="form-control" placeholder="Search Customer ID or Contract..." value={search} onChange={e => setSearch(e.target.value)} />
                    <select className="form-select" style={{ width: "160px" }} value={riskFilter} onChange={e => setRiskFilter(e.target.value)}>
                        <option value="All">All Risk Levels</option>
                        <option value="High Risk">High Risk</option>
                        <option value="Medium Risk">Medium Risk</option>
                        <option value="Low Risk">Low Risk</option>
                    </select>
                </div>
                <div style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
                    Showing Telco dataset sample records
                </div>
            </div>

            <div className="table-responsive">
                <table className="saas-table">
                    <thead>
                        <tr>
                            <th>Customer ID</th>
                            <th>Tenure</th>
                            <th>Contract Type</th>
                            <th>Monthly Spend</th>
                            <th>Total Lifetime Spend</th>
                            <th>Predicted Risk</th>
                            <th>Outcome</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.map(c => (
                            <tr key={c.id}>
                                <td style={{ fontWeight: 600 }}>{c.id}</td>
                                <td>{c.tenure} mos</td>
                                <td>{c.contract}</td>
                                <td>${c.charges.toFixed(2)}</td>
                                <td>${c.total.toFixed(2)}</td>
                                <td>
                                    <span className={`badge-risk ${c.risk === 'High Risk' ? 'high' : c.risk === 'Medium Risk' ? 'medium' : 'low'}`}>
                                        {c.risk} ({(c.prob * 100).toFixed(1)}%)
                                    </span>
                                </td>
                                <td>
                                    <span style={{ fontWeight: 600, color: c.status === 'Churned' ? 'var(--risk-high)' : 'var(--risk-low)' }}>
                                        {c.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 4: ANALYTICS PAGE
// ============================================================
function AnalyticsPage() {
    const chartRef = useRef(null);
    const chartInst = useRef(null);

    useEffect(() => {
        if (chartRef.current) {
            if (chartInst.current) chartInst.current.destroy();
            chartInst.current = new Chart(chartRef.current, {
                type: 'bar',
                data: {
                    labels: ['Fiber Optic', 'DSL', 'No Internet'],
                    datasets: [
                        { label: 'Churn Rate (%)', data: [41.8, 19.0, 7.4], backgroundColor: '#ef4444' },
                        { label: 'Retention Rate (%)', data: [58.2, 81.0, 92.6], backgroundColor: '#10b981' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
                    },
                    plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
                }
            });
        }
    }, []);

    return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-chart-column me-2 text-indigo"></i>Churn Rate by Internet Service Provider Type</h3>
                <div style={{ height: "320px" }}><canvas ref={chartRef}></canvas></div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "1.5rem" }}>
                <div className="card-panel">
                    <h4 className="form-section-title"><i className="fa-solid fa-lightbulb text-amber"></i> Key Empirical Discovery</h4>
                    <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem", lineHeight: 1.6 }}>
                        Customers subscribed to <strong>Fiber Optic internet</strong> exhibit a <strong>41.8% churn rate</strong>, compared to only 19.0% for DSL. Cross-referencing tech support reveals that Fiber Optic customers lacking Tech Support or Security add-ons experience the highest attrition.
                    </p>
                </div>
                <div className="card-panel">
                    <h4 className="form-section-title"><i className="fa-solid fa-shield text-green"></i> Retention Recommendations</h4>
                    <ul style={{ color: "var(--text-secondary)", fontSize: "0.875rem", paddingLeft: "1.2rem", lineHeight: 1.8 }}>
                        <li>Offer discounted 1-Year/2-Year contracts to Month-to-month subscribers.</li>
                        <li>Bundle Tech Support & Backup for Fiber Optic installations.</li>
                        <li>Incentivize automatic credit card / bank transfer payments over electronic checks.</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 5: PREDICTION HISTORY PAGE
// ============================================================
function HistoryPage({ history, setHistory }) {
    return (
        <div className="card-panel">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
                <h3 className="form-section-title" style={{ border: "none", margin: 0, padding: 0 }}>
                    <i className="fa-solid fa-clock-rotate-left me-2 text-indigo"></i>Session Prediction History Log
                </h3>
                {history.length > 0 && (
                    <button className="btn-secondary-saas" onClick={() => setHistory([])}>
                        <i className="fa-solid fa-trash me-1"></i> Clear History
                    </button>
                )}
            </div>

            <div className="table-responsive">
                <table className="saas-table">
                    <thead>
                        <tr>
                            <th>Prediction ID</th>
                            <th>Timestamp</th>
                            <th>Contract Type</th>
                            <th>Tenure</th>
                            <th>Monthly Spend</th>
                            <th>Prediction</th>
                            <th>Churn Probability</th>
                            <th>Risk Category</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.length === 0 ? (
                            <tr>
                                <td colSpan="8" style={{ textAlign: "center", padding: "3rem", color: "var(--text-muted)" }}>
                                    No predictions recorded in this browser session. Navigate to <strong>Predict Churn</strong> to perform inference.
                                </td>
                            </tr>
                        ) : (
                            history.map(item => (
                                <tr key={item.id}>
                                    <td style={{ fontWeight: 700 }}>{item.id}</td>
                                    <td>{item.timestamp}</td>
                                    <td>{item.contract}</td>
                                    <td>{item.tenure} mos</td>
                                    <td>${item.monthlyCharges.toFixed(2)}</td>
                                    <td style={{ fontWeight: 700, color: item.prediction === 'Yes' ? 'var(--risk-high)' : 'var(--risk-low)' }}>
                                        {item.prediction}
                                    </td>
                                    <td>{(item.probability * 100).toFixed(1)}%</td>
                                    <td>
                                        <span className={`badge-risk ${item.risk === 'High Risk' ? 'high' : item.risk === 'Medium Risk' ? 'medium' : 'low'}`}>
                                            {item.risk}
                                        </span>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 6: MODEL INSIGHTS PAGE
// ============================================================
function InsightsPage() {
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
            {/* Model Spec Card */}
            <div className="card-panel">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "1rem" }}>
                    <div>
                        <h3 style={{ fontSize: "1.35rem", fontWeight: 800, color: "var(--text-primary)" }}>
                            <i className="fa-solid fa-tree me-2 text-indigo"></i>Tuned Random Forest Classifier
                        </h3>
                        <p style={{ color: "var(--text-secondary)", fontSize: "0.875rem", marginTop: "0.25rem" }}>
                            Serialized Scikit-Learn Pipeline (`models/best_model_pipeline.joblib`)
                        </p>
                    </div>
                    <span className="badge-risk low" style={{ fontSize: "0.85rem", padding: "0.5rem 1rem" }}>
                        Active Production Model
                    </span>
                </div>

                {/* Empirical Test Metrics Grid */}
                <div className="kpi-grid" style={{ marginTop: "1.5rem", marginBottom: 0 }}>
                    <div className="card-panel kpi-card" style={{ background: "rgba(15,23,42,0.5)" }} title="Recall: Proportion of actual churners correctly caught">
                        <div className="kpi-icon green"><i className="fa-solid fa-bullseye"></i></div>
                        <div>
                            <div className="kpi-val">81.28%</div>
                            <div className="kpi-lbl">Test Set Recall (304 / 374)</div>
                        </div>
                    </div>
                    <div className="card-panel kpi-card" style={{ background: "rgba(15,23,42,0.5)" }} title="ROC-AUC Score: Area under Receiver Operating Characteristic Curve">
                        <div className="kpi-icon indigo"><i className="fa-solid fa-chart-area"></i></div>
                        <div>
                            <div className="kpi-val">0.8383</div>
                            <div className="kpi-lbl">ROC-AUC Score</div>
                        </div>
                    </div>
                    <div className="card-panel kpi-card" style={{ background: "rgba(15,23,42,0.5)" }} title="F1-Score: Harmonic mean of Precision and Recall">
                        <div className="kpi-icon amber"><i className="fa-solid fa-scale-balanced"></i></div>
                        <div>
                            <div className="kpi-val">0.6242</div>
                            <div className="kpi-lbl">F1-Score (Holdout Test)</div>
                        </div>
                    </div>
                    <div className="card-panel kpi-card" style={{ background: "rgba(15,23,42,0.5)" }} title="Accuracy: Total correct predictions over holdout test set">
                        <div className="kpi-icon red"><i className="fa-solid fa-check-double"></i></div>
                        <div>
                            <div className="kpi-val">73.99%</div>
                            <div className="kpi-lbl">Test Accuracy (1041 / 1407)</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Visual ML Pipeline Flowchart */}
            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-diagram-project me-2 text-indigo"></i>End-to-End Machine Learning Pipeline Architecture</h3>
                
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "1rem", margin: "1.5rem 0", textAlign: "center" }}>
                    <div style={{ background: "rgba(15,23,42,0.6)", padding: "1.25rem", borderRadius: "10px", border: "1px solid var(--border-color)" }}>
                        <i className="fa-solid fa-database fa-2x text-indigo mb-2"></i>
                        <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>1. Raw Data Input</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>21 Customer Features</div>
                    </div>

                    <div style={{ background: "rgba(15,23,42,0.6)", padding: "1.25rem", borderRadius: "10px", border: "1px solid var(--border-color)" }}>
                        <i className="fa-solid fa-gears fa-2x text-indigo mb-2"></i>
                        <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>2. Preprocessing</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>OneHot & StandardScaler</div>
                    </div>

                    <div style={{ background: "rgba(15,23,42,0.6)", padding: "1.25rem", borderRadius: "10px", border: "1px solid var(--border-color)" }}>
                        <i className="fa-solid fa-tree fa-2x text-indigo mb-2"></i>
                        <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>3. Random Forest</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>200 Balanced Trees</div>
                    </div>

                    <div style={{ background: "rgba(15,23,42,0.6)", padding: "1.25rem", borderRadius: "10px", border: "1px solid var(--border-color)" }}>
                        <i className="fa-solid fa-calculator fa-2x text-indigo mb-2"></i>
                        <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>4. Probability Scoring</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>0.0% to 100.0%</div>
                    </div>

                    <div style={{ background: "rgba(15,23,42,0.6)", padding: "1.25rem", borderRadius: "10px", border: "1px solid var(--border-color)" }}>
                        <i className="fa-solid fa-shield-cat fa-2x text-indigo mb-2"></i>
                        <div style={{ fontWeight: 700, fontSize: "0.9rem" }}>5. Risk Category</div>
                        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>Low / Medium / High</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 7: ABOUT & DOCS PAGE
// ============================================================
function AboutPage() {
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-book me-2 text-indigo"></i>About ChurnIQ & Project Architecture</h3>
                <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem", lineHeight: 1.7 }}>
                    <strong>ChurnIQ</strong> is an enterprise customer churn intelligence platform built using Python 3.14, Scikit-Learn pipelines, FastAPI REST backend, and a modern React frontend interface.
                </p>
            </div>

            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-code me-2 text-indigo"></i>REST API Documentation (POST /predict)</h3>
                
                <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid var(--border-color)", padding: "1rem", borderRadius: "8px", fontFamily: "monospace", fontSize: "0.85rem", color: "#a5b4fc", margin: "1rem 0" }}>
                    POST https://churniq-api-cds0.onrender.com/predict
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "1rem" }}>
                    <div>
                        <div style={{ fontWeight: 600, fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}>Sample Request Payload:</div>
                        <pre style={{ background: "#0b1329", padding: "1rem", borderRadius: "8px", color: "#67e8f9", fontSize: "0.8rem", overflowX: "auto" }}>
{`{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure": 1,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.35,
  "TotalCharges": 70.35
}`}
                        </pre>
                    </div>

                    <div>
                        <div style={{ fontWeight: 600, fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "0.5rem" }}>Sample API Response:</div>
                        <pre style={{ background: "#0b1329", padding: "1rem", borderRadius: "8px", color: "#4ade80", fontSize: "0.8rem", overflowX: "auto" }}>
{`{
  "prediction": "Yes",
  "churn_probability": 0.7877,
  "risk_level": "High Risk",
  "model_name": "RandomForestClassifier (Tuned)"
}`}
                        </pre>
                    </div>
                </div>
            </div>
        </div>
    );
}

// ============================================================
// PAGE 8: SETTINGS PAGE
// ============================================================
function SettingsPage({ apiConnected, checkApiHealth, theme, toggleTheme }) {
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem", maxWidth: "800px" }}>
            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-server me-2 text-indigo"></i>Backend API Configuration</h3>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "1rem", margin: "1rem 0" }}>
                    <div>
                        <div style={{ fontWeight: 600 }}>FastAPI Server URL</div>
                        <div style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>https://churniq-api-cds0.onrender.com</div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                        <span className={`badge-risk ${apiConnected ? 'low' : 'high'}`}>
                            {apiConnected ? 'Connected' : 'Offline'}
                        </span>
                        <button className="btn-secondary-saas" onClick={checkApiHealth}>Test Connection</button>
                    </div>
                </div>
            </div>

            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-palette me-2 text-indigo"></i>Appearance Preferences</h3>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", margin: "1rem 0" }}>
                    <div>
                        <div style={{ fontWeight: 600 }}>Theme Mode</div>
                        <div style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>Currently active: {theme.toUpperCase()} theme</div>
                    </div>
                    <button className="btn-primary-saas" onClick={toggleTheme}>
                        Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode
                    </button>
                </div>
            </div>

            <div className="card-panel">
                <h3 className="form-section-title"><i className="fa-solid fa-sliders me-2 text-indigo"></i>Application Specifications</h3>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", fontSize: "0.9rem", color: "var(--text-secondary)" }}>
                    <div><strong>App Version:</strong> v1.0.0</div>
                    <div><strong>ML Engine:</strong> Scikit-Learn 1.3+</div>
                    <div><strong>API Framework:</strong> FastAPI 0.142</div>
                    <div><strong>Frontend Engine:</strong> React 18</div>
                </div>
            </div>
        </div>
    );
}

// Render React Application Root
ReactDOM.render(<App />, document.getElementById("root"));
