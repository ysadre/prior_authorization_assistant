import React, { useState } from "react";
import "./index.css"; // Import CSS
import ReactMarkdown from "react-markdown";


function App() {
  const [healthPlan, setHealthPlan] = useState("Aetna");
  const [diagnosis, setDiagnosis] = useState("");
  const [customDiagnosis, setCustomDiagnosis] = useState("");
  const [procedure, setProcedure] = useState("");
  const [customProcedure, setCustomProcedure] = useState("");
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Diagnosis Options (Sorted Alphabetically)
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
  ].sort(); // Sort alphabetically

  // Procedure Options (Sorted Alphabetically)
  const procedures = [
    "3D Rendering for Spinal Imaging",
    "CT Procedures",
    "MRI/MRA Procedures",
    "Nuclear Medicine",
    "Spinal PET/CT",
    "Ultrasound",
  ].sort(); // Sort alphabetically

  const formatResponse = (text) => {
    if (!text) return "";
  
    // Remove markdown headers (####, ###, ##, #)
    text = text.replace(/^#+\s*/gm, "");
  
    // Convert **bold text** to <strong> tags
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  
    return text;
  };
  
  const handleSubmit = async () => {
    setError(null);
    setResponse(null);
    setLoading(true);

    const finalDiagnosis = diagnosis === "Other" ? customDiagnosis : diagnosis;
    const finalProcedure = procedure === "Other" ? customProcedure : procedure;

    if (!finalDiagnosis || !finalProcedure) {
      setError("Please enter a valid diagnosis and procedure.");
      setLoading(false);
      return;
    }

    const requestData = {
      health_plan: healthPlan,
      diagnosis: finalDiagnosis,
      procedure: finalProcedure,
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
      setResponse(data.response);
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

      {/* Diagnosis Dropdown */}
      <label>Diagnosis:</label>
      <select value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)}>
        <option value="">Select Diagnosis</option>
        {diagnoses.map((diag, index) => (
          <option key={index} value={diag}>
            {diag}
          </option>
        ))}
        <option value="Other">Other (Specify Below)</option>
      </select>

      {/* Custom Diagnosis Input */}
      {diagnosis === "Other" && (
        <input
          type="text"
          placeholder="Enter custom diagnosis"
          value={customDiagnosis}
          onChange={(e) => setCustomDiagnosis(e.target.value)}
          className="text-input"
        />
      )}

      {/* Procedure Dropdown */}
      <label>Procedure:</label>
      <select value={procedure} onChange={(e) => setProcedure(e.target.value)}>
        <option value="">Select Procedure</option>
        {procedures.map((proc, index) => (
          <option key={index} value={proc}>
            {proc}
          </option>
        ))}
        <option value="Other">Other (Specify Below)</option>
      </select>

      {/* Custom Procedure Input */}
      {procedure === "Other" && (
        <input
          type="text"
          placeholder="Enter custom procedure"
          value={customProcedure}
          onChange={(e) => setCustomProcedure(e.target.value)}
          className="text-input"
        />
      )}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Checking..." : "Check Prior Authorization"}
      </button>

      {error && <p className="error">{error}</p>}

      {response && (
        <div className="response-box">
          <h2>PA Guidelines</h2>
          <ReactMarkdown>{response}</ReactMarkdown>
        </div>
      )}

    </div>
  );
}

export default App;
