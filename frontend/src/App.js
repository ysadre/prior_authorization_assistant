import React, { useState, useEffect } from "react";
import "./index.css"; // Import CSS
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";


function App() {
  const [healthPlan, setHealthPlan] = useState("Aetna");
  const [diagnosis, setDiagnosis] = useState("");
  const [procedure, setProcedure] = useState("");
  const [filteredDiagnoses, setFilteredDiagnoses] = useState([]);
  const [filteredProcedures, setFilteredProcedures] = useState([]);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pages, setPages] = useState([]);
  const [selectedPage, setSelectedPage] = useState(null);
  const [activeDropdown, setActiveDropdown] = useState(null); // Tracks active dropdown


  // Diagnosis Options
  const diagnoses = [
    "Aortic Aneurysm or Dissection",
    "Cancer (Spinal Malignancy, Metastatic Disease)",
    "Cauda Equina Syndrome",
    "Fracture (Including Trauma-Related & Pathological)",
    "Lumbar Spine Spondylolysis/Spondylolisthesis",
    "Lumbar Spinal Stenosis",
    "Low Back (Lumbar Spine) Pain/Coccydynia",
    "Lower Extremity Pain with Neurological Features",
    "Motor Weakness",
    "Myelopathy",
    "Neck (Cervical Spine) Pain",
    "Post-Operative Spinal Disorders",
    "Sacral-Iliac (SI) Joint Pain",
    "Severe Radicular Pain",
    "Spinal Canal/Cord Disorders",
    "Spinal Compression Fractures",
    "Spinal Deformities",
    "Spinal Infection",
    "Spinal Pain Related to Cancer",
    "Upper Back (Thoracic Spine) Pain",
  ].sort();

  // Procedure Options
  const procedures = [
    "3D Rendering for Spinal Imaging",
    "CT Procedures",
    "MRI/MRA Procedures",
    "Nuclear Medicine",
    "Spinal PET/CT",
    "Ultrasound",
  ].sort();

  // Format AI Response
  const formatResponse = (text) => {
    if (!text) return "";
  
    // Remove Markdown headers
    text = text.replace(/^#+\s*/gm, "");

    // Convert **bold text** to <strong> tags
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    return text;
  };

  const handleDiagnosisChange = (e) => {
    const value = e.target.value;
    setDiagnosis(value);
  
    // Include the typed value as the first option in dropdown
    const filtered = diagnoses.filter(d => d.toLowerCase().includes(value.toLowerCase()));
    setFilteredDiagnoses(value ? [value, ...filtered] : diagnoses);
  };
  
  const handleProcedureChange = (e) => {
    const value = e.target.value;
    setProcedure(value);
  
    // Include the typed value as the first option in dropdown
    const filtered = procedures.filter(p => p.toLowerCase().includes(value.toLowerCase()));
    setFilteredProcedures(value ? [value, ...filtered] : procedures);
  };
  

  const handleDiagnosisFocus = () => {
    setFilteredDiagnoses(diagnoses);
    setFilteredProcedures([]); // Close procedure dropdown
    setActiveDropdown("diagnosis"); // Mark diagnosis as active
  };
  
  const handleProcedureFocus = () => {
    setFilteredProcedures(procedures);
    setFilteredDiagnoses([]); // Close diagnosis dropdown
    setActiveDropdown("procedure"); // Mark procedure as active
  };

  // Hide dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest(".dropdown-container")) {
        setFilteredDiagnoses([]);
        setFilteredProcedures([]);
        setActiveDropdown(null); // Reset active dropdown
      }
    };
  
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);
  

  const handleSubmit = async () => {
    setError(null);
    setResponse(null);
    setPages([]);
    setSelectedPage(null);
    setLoading(true);

    if (!diagnosis || !procedure) {
      setError("Please enter a valid diagnosis and procedure.");
      setLoading(false);
      return;
    }

    const requestData = {
      health_plan: healthPlan,
      diagnosis,
      procedure,
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(formatResponse(data.response));
      setPages(data.pages || []);
    } catch (err) {
      setError(`Failed to fetch data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Sigma Health: Prior Authorization Assistant</h1>

      <label>Health Plan:</label>
      <select value={healthPlan} onChange={(e) => setHealthPlan(e.target.value)}>
        <option value="Aetna">Aetna</option>
      </select>

      {/* Diagnosis Search Input */}
<label>Diagnosis:</label>
<div className="dropdown-container">
  <input
    type="text"
    placeholder="Enter a diagnosis"
    value={diagnosis}
    onChange={handleDiagnosisChange}
    onFocus={handleDiagnosisFocus}
    className="text-input"
  />
  {activeDropdown === "diagnosis" && filteredDiagnoses.length > 0 && (
    <ul className="dropdown">
      {filteredDiagnoses.map((d, index) => (
        <li key={index} onClick={() => { setDiagnosis(d); setFilteredDiagnoses([]); setActiveDropdown(null); }}>
          {d}
        </li>
      ))}
    </ul>
  )}
</div>

{/* Procedure Search Input */}
<label>Procedure:</label>
<div className="dropdown-container">
  <input
    type="text"
    placeholder="Enter a procedure"
    value={procedure}
    onChange={handleProcedureChange}
    onFocus={handleProcedureFocus}
    className="text-input"
  />
  {activeDropdown === "procedure" && filteredProcedures.length > 0 && (
    <ul className="dropdown">
      {filteredProcedures.map((p, index) => (
        <li key={index} onClick={() => { setProcedure(p); setFilteredProcedures([]); setActiveDropdown(null); }}>
          {p}
        </li>
      ))}
    </ul>
  )}
</div>



      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Check Prior Authorization"}
      </button>

      {error && <p className="error">{error}</p>}

  {response && (
    <div className="response-box">
      <h2>PA Guidelines</h2>
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {response}
      </ReactMarkdown>
    </div>
  )}
  


      {pages.length > 0 && (
        <div>
          <label>Source Page:</label>
          <select value={selectedPage} onChange={(e) => setSelectedPage(e.target.value)}>
            <option value="">Select a page</option>
            {pages.map((page, index) => (
              <option key={index} value={page}>
                Page {page}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}

export default App;
