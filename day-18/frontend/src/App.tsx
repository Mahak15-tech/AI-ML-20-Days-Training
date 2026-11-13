import { useEffect, useRef, useState, type ChangeEvent, type DragEvent } from "react";
import {
  ArrowDown,
  ArrowDownToLine,
  ArrowRight,
  ArrowUpRight,
  Activity,
  Check,
  CircleAlert,
  CloudUpload,
  Crosshair,
  Cpu,
  FileImage,
  LoaderCircle,
  Menu,
  Moon,
  ScanLine,
  ShieldCheck,
  Sparkles,
  Sun,
  Trash2,
  Upload,
  X,
  Zap,
} from "lucide-react";

import streetImage from "./assets/street-detection.jpg";
import chipImage from "./assets/vision-chip.jpg";
import aboutImage from "./assets/about-studio.jpg";

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

type Detection = {
  class_id: number;
  class_name: string;
  confidence: number;
  bounding_box: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
};

type Prediction = {
  success: boolean;
  filename: string;
  image_width: number;
  image_height: number;
  confidence_threshold: number;
  inference_time_ms: number;
  objects_detected: number;
  detections: Detection[];
  annotated_image_url: string;
};

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [apiOnline, setApiOnline] = useState(false);
  const [checkingApi, setCheckingApi] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [confidence, setConfidence] = useState(0.25);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragging, setDragging] = useState(false);
  const [showAnnotated, setShowAnnotated] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let active = true;

    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        if (active) setApiOnline(response.ok && data.model_loaded === true);
      } catch {
        if (active) setApiOnline(false);
      } finally {
        if (active) setCheckingApi(false);
      }
    };

    checkHealth();
    const interval = window.setInterval(checkHealth, 30000);

    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    return () => {
      if (preview.startsWith("blob:")) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const scrollTo = (id: string) => {
    setMobileOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  const selectFile = (selected?: File) => {
    if (!selected) return;

    if (!selected.type.startsWith("image/")) {
      setError("Please select a valid image file.");
      return;
    }

    if (selected.size > 15 * 1024 * 1024) {
      setError("Please choose an image smaller than 15 MB.");
      return;
    }

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setPrediction(null);
    setError("");
    setShowAnnotated(false);
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    selectFile(event.target.files?.[0]);
    event.target.value = "";
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    selectFile(event.dataTransfer.files[0]);
  };

  const runDetection = async () => {
    if (!file || loading) return;

    setLoading(true);
    setError("");
    setPrediction(null);
    setShowAnnotated(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_BASE}/predict?conf=${confidence}`,
        {
          method: "POST",
          body: formData,
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Detection failed. Please try another image.",
        );
      }

      setPrediction(data as Prediction);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the detection server.",
      );
    } finally {
      setLoading(false);
    }
  };

  const clearWorkspace = () => {
    setFile(null);
    setPreview("");
    setPrediction(null);
    setError("");
    setShowAnnotated(false);
    if (inputRef.current) inputRef.current.value = "";
  };

  const annotatedUrl = prediction
    ? `${API_BASE}${prediction.annotated_image_url}`
    : "";

  const displayedImage =
    prediction && showAnnotated ? annotatedUrl : preview;

  
const downloadResult = async () => {
  if (!annotatedUrl) return;

  try {
    const response = await fetch(annotatedUrl);

    if (!response.ok) {
      throw new Error("Failed to download the detected image.");
    }

    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);

    const originalName = file?.name || "detection";
    const cleanName = originalName.replace(/\.[^/.]+$/, "");

    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = `yolo-${cleanName}-detected.jpg`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(objectUrl);
  } catch (error) {
    console.error("Download failed:", error);
    setError("Unable to download the detected image. Please try again.");
  }
};


  const counts = prediction
    ? Object.entries(
        prediction.detections.reduce<Record<string, number>>((acc, item) => {
          acc[item.class_name] = (acc[item.class_name] || 0) + 1;
          return acc;
        }, {}),
      ).sort((a, b) => b[1] - a[1])
    : [];

  return (
    <main className={`app-shell ${darkMode ? "dark-theme" : "light-theme"}`}>
      <header className="topbar">
        <a className="brand" href="#home" aria-label="YOLO Studio home">
          <span className="brand-symbol"><ScanLine size={21} /></span>
          <span>YOLO<span className="brand-light">Studio</span></span>
        </a>

        <nav className={`nav-links ${mobileOpen ? "nav-open" : ""}`}>
          <button onClick={() => scrollTo("features")}>Platform</button>
          <button onClick={() => scrollTo("technology")}>Technology</button>
          <button onClick={() => scrollTo("workspace")}>Workspace</button>
          <button onClick={() => scrollTo("about")}>About</button>
        </nav>

        <div className="topbar-actions">
          <span className={`api-indicator ${apiOnline ? "online" : "offline"}`}>
            <i />
            {checkingApi ? "Connecting" : apiOnline ? "System online" : "API offline"}
          </span>
          <button
            className="icon-button theme-button"
            onClick={() => setDarkMode(!darkMode)}
            aria-label="Toggle appearance"
          >
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
          </button>
          <button className="nav-cta" onClick={() => scrollTo("workspace")}>
            Launch studio <ArrowUpRight size={16} />
          </button>
          <button
            className="icon-button mobile-menu"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle menu"
          >
            {mobileOpen ? <X /> : <Menu />}
          </button>
        </div>
      </header>

      <section className="hero" id="home">
        <div className="hero-content">
          <div className="eyebrow">
            <span className="eyebrow-line" />
            COMPUTER VISION / REIMAGINED
          </div>

          <h1>
            Give your images
            <br />
            <span>a new perspective.</span>
          </h1>

          <p className="hero-description">
            Turn pixels into insights. Explore object detection with a
            fine-tuned YOLOv8 model, through one beautifully simple workspace.
          </p>

          <div className="hero-actions">
            <button className="primary-button" onClick={() => scrollTo("workspace")}>
              Explore the studio <ArrowUpRight size={18} />
            </button>
            <button className="text-button" onClick={() => scrollTo("technology")}>
              Discover the technology <ArrowRight size={17} />
            </button>
          </div>

          <div className="hero-footnote">
            <span><ShieldCheck size={16} /> Powered by your fine-tuned YOLOv8n model</span>
            <span className="footnote-divider" />
            <span>Built for exploration</span>
          </div>
        </div>

        <div className="hero-visual">
          <div className="hero-image-frame">
            <img src={streetImage} alt="Urban street scene for computer vision" />
            <div className="hero-image-overlay" />
            <div className="hero-image-top">
              <span><span className="live-dot" /> VISUAL INTELLIGENCE</span>
              <span>01 / 03</span>
            </div>
            <div className="hero-image-bottom">
              <div>
                <small>THE WORLD, IN DATA</small>
                <h3>Every detail<br />has a story.</h3>
              </div>
              <span className="round-arrow"><ArrowUpRight size={23} /></span>
            </div>
          </div>
          <div className="hero-side-note">
            <span className="side-note-number">01</span>
            <span>Observe<br />Understand<br />Discover</span>
          </div>
          <div className="hero-stamp"><ScanLine size={22} /><span>YOLO<br />VISION</span></div>
        </div>

        <div className="hero-bottom">
          <span>01 — INTRODUCTION</span>
          <span>SCROLL TO EXPLORE <ArrowDown size={15} /></span>
        </div>
      </section>

      <section className="intro-strip" id="features">
        <div className="intro-heading">
          <span className="section-index">01 / THE PLATFORM</span>
          <h2>
            Intelligence that
            <br />
            <em>feels effortless.</em>
          </h2>
        </div>
        <div className="intro-right">
          <p>
            Powerful computer vision doesn't need a complicated interface.
            YOLO Studio brings image analysis, model inference and visual
            results together in one focused experience.
          </p>
          <div className="feature-grid">
            <article className="feature-card">
              <span className="feature-icon"><Zap /></span>
              <span className="feature-number">01</span>
              <h3>Real model inference</h3>
              <p>Send images directly to your fine-tuned YOLOv8 model.</p>
            </article>
            <article className="feature-card">
              <span className="feature-icon"><Crosshair /></span>
              <span className="feature-number">02</span>
              <h3>Visual detections</h3>
              <p>Explore model-generated bounding boxes and class confidence.</p>
            </article>
            <article className="feature-card">
              <span className="feature-icon"><ArrowDownToLine /></span>
              <span className="feature-number">03</span>
              <h3>Export your results</h3>
              <p>Download the annotated image generated by the backend.</p>
            </article>
          </div>
        </div>
      </section>

      <section className="studio-section" id="workspace">
        <div className="studio-heading">
          <div>
            <span className="section-index">02 / INTERACTIVE WORKSPACE</span>
            <h2>Make the invisible <em>visible.</em></h2>
            <p>Your image in. Actionable visual results out.</p>
          </div>
          <div className="studio-model-tag">
            <span className="model-icon"><Cpu size={18} /></span>
            <span><b>YOLOv8n</b><small>Fine-tuned model</small></span>
          </div>
        </div>

        <div className="studio-layout">
          <div className="studio-main">
            <div className="studio-toolbar">
              <div className="toolbar-title">
                <span className="toolbar-icon"><ScanLine size={17} /></span>
                <span>Detection workspace</span>
              </div>
              <div className="toolbar-status">
                <i className={apiOnline ? "online" : "offline"} />
                {apiOnline ? "Backend connected" : "Backend unavailable"}
              </div>
            </div>

            <div
              className={`image-stage ${dragging ? "drag-active" : ""} ${!preview ? "empty-stage" : ""}`}
              onDragOver={(event) => {
                event.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
            >
              {preview ? (
                <>
                  <img
                    className="stage-image"
                    src={displayedImage}
                    alt="Selected image or annotated detection result"
                  />
                  <div className="image-stage-tools">
                    <span><FileImage size={14} /> {file?.name}</span>
                    {prediction && (
                      <button
                        onClick={() => setShowAnnotated(!showAnnotated)}
                        className="view-toggle"
                      >
                        {showAnnotated ? "Annotated view" : "Original image"}
                      </button>
                    )}
                  </div>
                </>
              ) : (
                <div className="upload-prompt">
                  <div className="upload-graphic">
                    <span className="upload-orbit orbit-a" />
                    <span className="upload-orbit orbit-b" />
                    <CloudUpload size={32} strokeWidth={1.5} />
                  </div>
                  <h3>Start with an image.</h3>
                  <p>Drag and drop your image here, or browse your device.</p>
                  <button className="upload-button" onClick={() => inputRef.current?.click()}>
                    <Upload size={16} /> Choose an image
                  </button>
                  <span className="upload-hint">JPG, PNG, WEBP · Maximum 15 MB</span>
                </div>
              )}

              {loading && (
                <div className="processing-overlay">
                  <div className="processing-card">
                    <LoaderCircle className="spin-icon" size={30} />
                    <b>Analysing your image</b>
                    <span>Running YOLOv8 inference...</span>
                  </div>
                </div>
              )}
            </div>

            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              hidden
              onChange={handleFileChange}
            />

            <div className="studio-controls">
              <div className="confidence-control">
                <label htmlFor="confidence">
                  Confidence threshold <b>{Math.round(confidence * 100)}%</b>
                </label>
                <input
                  id="confidence"
                  type="range"
                  min="0.05"
                  max="0.95"
                  step="0.05"
                  value={confidence}
                  onChange={(event) => setConfidence(Number(event.target.value))}
                />
                <div className="range-labels"><span>More detections</span><span>Higher confidence</span></div>
              </div>

              <div className="studio-buttons">
                <button
                  className="clear-button"
                  onClick={clearWorkspace}
                  disabled={!file || loading}
                  title="Clear workspace"
                >
                  <Trash2 size={16} />
                </button>
                <button
                  className="run-button"
                  onClick={runDetection}
                  disabled={!file || loading || !apiOnline}
                >
                  {loading ? <LoaderCircle className="spin-icon" size={17} /> : <Crosshair size={17} />}
                  {loading ? "Processing..." : "Run detection"}
                  {!loading && <ArrowRight size={17} />}
                </button>
              </div>
            </div>

            {error && (
              <div className="error-message">
                <CircleAlert size={17} /> {error}
              </div>
            )}
          </div>

          <aside className="results-panel">
            <div className="results-header">
              <div>
                <span className="section-index">LIVE ANALYSIS</span>
                <h3>Detection report</h3>
              </div>
              <Activity size={19} />
            </div>

            {prediction ? (
              <>
                <div className="result-total">
                  <span>Objects detected</span>
                  <strong>{prediction.objects_detected.toString().padStart(2, "0")}</strong>
                  <small>From the current image</small>
                </div>

                <div className="result-metrics">
                  <div>
                    <span>Inference time</span>
                    <b>{prediction.inference_time_ms.toFixed(1)} <small>ms</small></b>
                  </div>
                  <div>
                    <span>Image resolution</span>
                    <b>{prediction.image_width} × {prediction.image_height}</b>
                  </div>
                </div>

                <div className="detection-list-heading">
                  <span>DETECTED CLASSES</span>
                  <span>{counts.length} classes</span>
                </div>

                <div className="detection-list">
                  {prediction.detections.length ? (
                    prediction.detections.map((item, index) => (
                      <div className="detection-item" key={`${item.class_id}-${index}`}>
                        <span className="detection-index">{String(index + 1).padStart(2, "0")}</span>
                        <span className="detection-name">{item.class_name}</span>
                        <span className="detection-confidence">
                          {(item.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="no-detections">No objects found above this confidence threshold.</p>
                  )}
                </div>

                <button className="download-button" onClick={downloadResult}>
                  <ArrowDownToLine size={17} /> Download annotated image
                </button>
              </>
            ) : (
              <div className="empty-results">
                <div className="empty-results-icon"><Crosshair size={25} /></div>
                <h4>Waiting for your image</h4>
                <p>
                  Your model results will appear here after you run detection.
                  Class labels and confidence scores come directly from the API.
                </p>
                <div className="empty-result-line"><span /> Model ready when you are</div>
              </div>
            )}
          </aside>
        </div>

        <div className="studio-footnote">
          <span><ShieldCheck size={15} /> Results generated by your local inference API</span>
          <span>Confidence threshold: {Math.round(confidence * 100)}%</span>
        </div>
      </section>

      <section className="technology-section" id="technology">
        <div className="technology-image">
          <img src={chipImage} alt="Computer vision processor concept" loading="lazy" />
          <span className="technology-image-caption">THE ENGINE BEHIND THE EXPERIENCE</span>
        </div>
        <div className="technology-copy">
          <span className="section-index">03 / THE TECHNOLOGY</span>
          <h2>Built on vision.<br /><em>Driven by intelligence.</em></h2>
          <p>
            At the heart of YOLO Studio is a fine-tuned YOLOv8n model.
            The FastAPI backend handles image processing and inference,
            returning detection coordinates, confidence scores and an
            annotated image to the interface.
          </p>
          <div className="technology-points">
            <div><span><Check size={16} /></span><p><b>Fine-tuned YOLOv8n</b><small>Your trained model weights</small></p></div>
            <div><span><Check size={16} /></span><p><b>FastAPI inference service</b><small>Real image upload and prediction</small></p></div>
            <div><span><Check size={16} /></span><p><b>Visual output pipeline</b><small>Coordinates, labels and annotated images</small></p></div>
          </div>
          <button className="text-button" onClick={() => scrollTo("workspace")}>
            Try the model <ArrowUpRight size={17} />
          </button>
        </div>
      </section>

      <section className="about-section" id="about">
        <div className="about-copy">
          <span className="section-index">04 / ABOUT THE PROJECT</span>
          <h2>Making computer vision<br /><em>more approachable.</em></h2>
          <p>
            YOLO Studio is an interactive computer vision project designed
            to make object detection easier to explore. It combines a
            responsive React interface with a Python inference backend,
            bringing model predictions into a practical visual workspace.
          </p>
          <button className="primary-button" onClick={() => scrollTo("workspace")}>
            Experience the studio <ArrowUpRight size={18} />
          </button>
        </div>
        <div className="about-visual">
          <img src={aboutImage} alt="Creative workspace for computer vision" loading="lazy" />
          <div className="about-visual-note">
            <Sparkles size={17} />
            <span>Curiosity meets<br /><b>computer vision.</b></span>
          </div>
        </div>
      </section>

      <footer className="footer">
        <a className="brand" href="#home">
          <span className="brand-symbol"><ScanLine size={20} /></span>
          <span>YOLO<span className="brand-light">Studio</span></span>
        </a>
        <p>See beyond the pixels.</p>
        <button onClick={() => scrollTo("home")}>Back to top <ArrowUpRight size={16} /></button>
        <span className="footer-copy">YOLO STUDIO · DAY 18 COMPUTER VISION PROJECT</span>
      </footer>
    </main>
  );
}

export default App;
