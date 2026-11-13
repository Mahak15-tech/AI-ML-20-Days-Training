import { useEffect, useRef, useState, type ChangeEvent } from "react";
import type { CSSProperties } from "react";
import {
  ArrowDownToLine,
  ArrowRight,
  ArrowUpRight,
  Box,
  Check,
  ChevronRight,
  CloudUpload,
  Crosshair,
  ImagePlus,
  Menu,
  Moon,
  Play,
  ScanLine,
  Sparkles,
  Sun,
  X,
  Zap,
} from "lucide-react";
import streetImage from "./assets/street-detection.jpg";
import workspaceImage from "./assets/workspace-detection.jpg";
import chipImage from "./assets/vision-chip.jpg";
import sunsetImage from "./assets/sunset-journey.jpg";
import aboutStudioImage from "./assets/about-studio.jpg";
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: string;
  size?: string;
};

function Button({
  children,
  className = "",
  variant: _variant,
  size: _size,
  ...props
}: ButtonProps) {
  return (
    <button className={className} {...props}>
      {children}
    </button>
  );
}
const features = [
  {
    icon: Zap,
    title: "Real-time detection",
    text: "Get instant results with YOLO’s blazing speed.",
  },
  { icon: Box, title: "Multiple classes", text: "Detect 80+ object classes with high accuracy." },
  {
    icon: ArrowDownToLine,
    title: "Easy download",
    text: "Save your annotated images in one click.",
  },
];

const steps = [
  {
    icon: CloudUpload,
    title: (
      <>
        Upload
        <br />
        your image
      </>
    ),
    text: "Choose an image from your device.",
  },
  {
    icon: ScanLine,
    title: (
      <>
        Let YOLO
        <br />
        do its magic
      </>
    ),
    text: "Our model detects objects instantly.",
  },
  {
    icon: ArrowDownToLine,
    title: (
      <>
        Explore
        <br />
        your results
      </>
    ),
    text: "View, analyze and download.",
  },
];

const reviews = [
  {
    initials: "SC",
    name: "Sarah Chen",
    role: "AI student",
    quote: "YOLO Studio makes object detection so easy and fun to use!",
  },
  {
    initials: "AK",
    name: "Alex Kumar",
    role: "Developer",
    quote: "Incredible tool! Fast, accurate and beautiful.",
  },
  {
    initials: "PS",
    name: "Priya Sharma",
    role: "Researcher",
    quote: "A must-have for anyone working with computer vision.",
  },
];

function HomePage() {
  const [darkMode, setDarkMode] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [imageUrl, setImageUrl] = useState<string>(workspaceImage);
  const [isScanning, setIsScanning] = useState(false);
  const [detected, setDetected] = useState(true);
  const [dragging, setDragging] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const items = document.querySelectorAll<HTMLElement>(".reveal");
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      items.forEach((item) => item.classList.add("is-visible"));
      return;
    }
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        }),
      { threshold: 0.12 },
    );
    items.forEach((item) => observer.observe(item));
    return () => observer.disconnect();
  }, []);

  const scrollTo = (id: string) => {
    setMobileOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  };

  const readFile = (file?: File) => {
    if (!file || !file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") {
        setImageUrl(reader.result);
        setDetected(false);
      }
    };
    reader.readAsDataURL(file);
  };

  const onFileChange = (event: ChangeEvent<HTMLInputElement>) => readFile(event.target.files?.[0]);

  const runDetection = () => {
    if (isScanning) return;
    setIsScanning(true);
    setDetected(false);
    window.setTimeout(() => {
      setIsScanning(false);
      setDetected(true);
    }, 1500);
  };

  return (
    <main className={`site-shell${darkMode ? " theme-dark" : ""}`}>
      <header className="site-header">
        <a className="brand" href="#home" aria-label="YOLO Studio home">
          <span className="brand-mark">
            <ScanLine size={20} strokeWidth={2.3} />
          </span>
          <span>
            YOLO <b>Studio</b>
          </span>
        </a>
        <nav className={mobileOpen ? "main-nav nav-open" : "main-nav"} aria-label="Main navigation">
          <button onClick={() => scrollTo("features")}>Features</button>
          <button onClick={() => scrollTo("how-it-works")}>How it works</button>
          <button onClick={() => scrollTo("technology")}>Model info</button>
          <button onClick={() => scrollTo("about")}>About</button>
          <Button className="mobile-nav-cta" onClick={() => scrollTo("workspace")}>
            Start detecting <ArrowRight />
          </Button>
        </nav>
        <div className="header-actions">
          <Button
            variant="ghost"
            size="icon"
            className="theme-toggle"
            aria-label={darkMode ? "Switch to light appearance" : "Switch to dark appearance"}
            onClick={() => setDarkMode(!darkMode)}
          >
            {darkMode ? (
              <Sun />
            ) : (
              <>
                <Sun />
                <Moon />
              </>
            )}
          </Button>
          <Button className="header-cta" onClick={() => scrollTo("workspace")}>
            Start detecting <ArrowRight />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="menu-toggle"
            aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X /> : <Menu />}
          </Button>
        </div>
      </header>

      <section className="hero section-light" id="home">
        <div className="hero-copy">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> Computer vision, reimagined
          </div>
          <h1>
            See the world
            <br />
            <em>differently.</em>
          </h1>
          <p className="hero-kicker">Powerful. Precise. Effortless.</p>
          <p className="hero-description">
            YOLO Studio brings the power of real-time object detection to your fingertips.
          </p>
          <div className="hero-buttons">
            <Button className="button-orange" onClick={() => scrollTo("workspace")}>
              Start detecting <ArrowRight />
            </Button>
            <button className="demo-link" onClick={() => scrollTo("workspace")}>
              <span>
                <Play size={15} fill="currentColor" />
              </span>{" "}
              Watch demo
            </button>
          </div>
          <div className="hero-sparkle sparkle-one">✳</div>
          <div className="hero-sparkle sparkle-two">✳</div>
        </div>
        <div className="hero-visual">
          <img
            className="hero-photo"
            src={streetImage}
            alt="A city street with cars and pedestrians for object detection"
            width={1536}
            height={1024}
            fetchPriority="high"
          />
          <div className="hero-image-shade" />
          <span className="detection-label label-car">
            car <b>0.94</b>
          </span>
          <span className="detection-box box-car" />
          <span className="detection-label label-person">
            person <b>0.93</b>
          </span>
          <span className="detection-box box-person" />
          <span className="detection-label label-bus">
            bus <b>0.91</b>
          </span>
          <span className="detection-box box-bus" />
          <div className="visual-metrics">
            <div>
              <Crosshair />
              <b>98.7%</b>
              <small>mAP@0.5</small>
            </div>
            <div>
              <Zap fill="currentColor" />
              <b>12ms</b>
              <small>Inference</small>
            </div>
            <div>
              <Box />
              <b>80+</b>
              <small>Classes</small>
            </div>
          </div>
        </div>
        <a className="scroll-cue" href="#features" aria-label="Scroll to features">
          <ArrowRight size={15} />
        </a>
      </section>

      <section className="features section-light" id="features">
        <div className="section-heading reveal">
          <div className="section-title">
            <div className="eyebrow">
              <Sparkles size={14} fill="currentColor" /> Power-packed features
            </div>
            <h2>
              Everything you need.
              <br />
              <em>Nothing in your way.</em>
            </h2>
          </div>
          <p className="section-intro">
            Advanced capabilities wrapped
            <br />
            in a simple, beautiful interface.
          </p>
        </div>
        <div className="features-row">
          <div className="feature-art reveal">
            <img
              src={streetImage}
              alt="AI object detection finding a car"
              width={1536}
              height={1024}
              loading="lazy"
            />
            <div className="mini-detection-box">
              <span>
                car <b>0.95</b>
              </span>
            </div>
            <span className="ai-pill">
              <Sparkles size={12} /> AI powered
            </span>
            <span className="art-star">✳</span>
          </div>
          <div className="feature-cards">
            {features.map(({ icon: Icon, title, text }, index) => (
              <article
                className="feature-card reveal"
                key={title}
                style={{ "--reveal-delay": `${index * 110}ms` } as CSSProperties}
              >
                <span className="icon-disc">
                  <Icon size={22} strokeWidth={2.2} />
                </span>
                <h3>{title}</h3>
                <p>{text}</p>
                <span className="card-arrow">
                  <ArrowRight size={13} />
                </span>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="how section-light" id="how-it-works">
        <div className="how-copy reveal">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> How it works
          </div>
          <h2>
            From image
            <br />
            to insights in
            <br />
            <em>seconds.</em>
          </h2>
          <p>A simple 3-step process to help you explore the power of YOLO.</p>
          <Button className="button-orange" onClick={() => scrollTo("workspace")}>
            Try it now <ArrowRight />
          </Button>
        </div>
        <div className="steps-row">
          {steps.map(({ icon: Icon, title, text }, index) => (
            <div
              className="step-wrap reveal"
              key={index}
              style={{ "--reveal-delay": `${index * 130}ms` } as CSSProperties}
            >
              <article className="step-card">
                <span className="step-number">0{index + 1}</span>
                <span className="step-icon">
                  <Icon size={34} strokeWidth={1.8} />
                </span>
                <h3>{title}</h3>
                <p>{text}</p>
              </article>
              {index < 2 && (
                <span className="step-arrow">
                  <ChevronRight size={16} />
                </span>
              )}
            </div>
          ))}
        </div>
      </section>

      <section className="workspace-section section-dark" id="workspace">
        <div className="workspace-copy reveal">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> Your creative workspace
          </div>
          <h2>
            Ready to find
            <br />
            <em>
              what’s in your
              <br />
              image?
            </em>
          </h2>
          <p>Upload, detect and explore with our powerful YOLO model.</p>
          <div className="workspace-buttons">
            <Button className="button-orange" onClick={() => fileInput.current?.click()}>
              <ImagePlus /> Upload an image
            </Button>
            <input
              ref={fileInput}
              className="file-input"
              type="file"
              accept="image/*"
              onChange={onFileChange}
            />
          </div>
        </div>
        <div
          className={`workspace-window reveal${dragging ? " is-dragging" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(event) => {
            event.preventDefault();
            setDragging(false);
            readFile(event.dataTransfer.files[0]);
          }}
        >
          <div className="window-topbar">
            <span className="window-dots">
              <i />
              <i />
              <i />
            </span>
            <span className="window-title">YOLO Vision · Workspace</span>
            <span className="live-status">
              <i /> {isScanning ? "Analyzing" : "Ready"}
            </span>
          </div>
          <div className="workspace-canvas">
            <img
              src={imageUrl}
              alt="Image open in the YOLO detection workspace"
              width={1536}
              height={1024}
            />
            <div className="canvas-tint" />
            {detected && (
              <div className="canvas-detections">
                <span className="canvas-label person-label">person 0.96</span>
                <span className="canvas-box person-box" />
                <span className="canvas-label person-label two">person 0.93</span>
                <span className="canvas-box person-box two" />
                <span className="canvas-label car-label">car 0.92</span>
                <span className="canvas-box car-box" />
              </div>
            )}
            {isScanning && <div className="scan-line" />}
            {isScanning && (
              <div className="scanning-message">
                <ScanLine /> Finding objects…
              </div>
            )}
            <button
              className="canvas-upload"
              aria-label="Upload an image"
              onClick={() => fileInput.current?.click()}
            >
              <CloudUpload size={16} />
            </button>
          </div>
          <div className="window-footer">
            <div className="result-status">
              <span className={`status-dot${detected ? "" : " status-idle"}`} />
              {detected ? "3 objects detected" : "Ready to analyze"}
            </div>
            <div className="window-controls">
              <span>YOLOv8 · 640 × 427</span>
              <Button className="detect-button" onClick={runDetection} disabled={isScanning}>
                {isScanning ? (
                  <>
                    <ScanLine /> Analyzing…
                  </>
                ) : (
                  <>
                    <Crosshair /> Detect objects <ArrowRight />
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
        <div className="realtime-pill">
          <span>
            <Sparkles size={16} />
          </span>
          <div>
            <b>Real-time results</b>
            <small>Powered by YOLOv8</small>
          </div>
        </div>
      </section>

      <section className="technology section-dark" id="technology">
        <div className="technology-copy reveal">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> The technology
          </div>
          <h2>
            Powered by
            <br />
            <em>YOLOv8.</em>
          </h2>
          <p>Cutting-edge AI. Real-world performance.</p>
          <ul>
            <li>
              <Check /> State-of-the-art model
            </li>
            <li>
              <Check /> High accuracy &amp; speed
            </li>
            <li>
              <Check /> Supports 80+ classes
            </li>
          </ul>
          <div className="tech-stats">
            <div>
              <Box />
              <b>80+</b>
              <small>Classes</small>
            </div>
            <div>
              <Zap />
              <b>11ms</b>
              <small>Speed</small>
            </div>
            <div>
              <Crosshair />
              <b>95.7%</b>
              <small>Accuracy</small>
            </div>
          </div>
        </div>
        <div className="chip-art reveal">
          <img
            src={chipImage}
            alt="A glowing AI vision processor"
            width={1536}
            height={1024}
            loading="lazy"
          />
          <span className="chip-orbit orbit-one" />
          <span className="chip-orbit orbit-two" />
          <span className="chip-sparkle">✳</span>
        </div>
      </section>

      <section className="about-section section-light" id="about">
        <div className="about-image" aria-hidden="true">
          <img
            src={aboutStudioImage}
            alt="A sunlit creative studio with a laptop displaying computer vision detections"
            width={1600}
            height={1104}
            loading="lazy"
          />
          <div className="about-image-wash" />
          <div className="about-floating-tag about-tag-detection">
            <span>
              <Zap size={20} fill="currentColor" />
            </span>
            <b>
              Real-Time
              <br />
              Detection
            </b>
          </div>
          <div className="about-floating-tag about-tag-model">
            <span>
              <Box size={20} />
            </span>
            <b>
              Powered by
              <br />
              YOLOv8
            </b>
          </div>
        </div>
        <div className="about-copy reveal">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> About YOLO Studio
          </div>
          <h2>
            Built for a<br />
            <em>Smarter Vision</em>
          </h2>
          <p className="about-lead">
            YOLO Studio is a modern, high-performance object detection platform powered by YOLOv8 —
            designed to make AI accessible, fast and effortless.
          </p>
          <span className="about-rule" />
          <p>
            Whether you’re a developer, researcher or creator, our platform helps you detect,
            explore and analyze objects in images with unmatched precision.
          </p>
          <Button className="button-orange" onClick={() => scrollTo("features")}>
            <Sparkles size={15} /> Explore features <ArrowRight />
          </Button>
        </div>
        <div className="about-stats reveal">
          <div>
            <span className="about-stat-icon">
              <Crosshair />
            </span>
            <div>
              <b>99.2%</b>
              <small>Detection accuracy</small>
            </div>
          </div>
          <div>
            <span className="about-stat-icon">
              <Zap fill="currentColor" />
            </span>
            <div>
              <b>12ms</b>
              <small>Inference speed</small>
            </div>
          </div>
          <div>
            <span className="about-stat-icon">
              <Box />
            </span>
            <div>
              <b>80+</b>
              <small>Classes supported</small>
            </div>
          </div>
          <div>
            <span className="about-stat-icon">
              <ScanLine />
            </span>
            <div>
              <b>Open source</b>
              <small>Community driven</small>
            </div>
          </div>
        </div>
      </section>

      <section className="reviews section-light" id="reviews">
        <div className="reviews-copy reveal">
          <div className="eyebrow">
            <Sparkles size={14} fill="currentColor" /> Loved by creators &amp; innovators
          </div>
          <h2>What our users say</h2>
          <p>Real feedback from a growing community of developers, students and visionaries.</p>
          <div className="review-cards">
            {reviews.map((review, index) => (
              <article
                className="review-card reveal"
                key={review.name}
                style={{ "--reveal-delay": `${index * 90}ms` } as CSSProperties}
              >
                <div className={`avatar avatar-${index}`}>{review.initials}</div>
                <b className="review-name">{review.name}</b>
                <span className="review-role">{review.role}</span>
                <p>“{review.quote}”</p>
                <div className="stars" aria-label="5 out of 5 stars">
                  ★★★★★
                </div>
              </article>
            ))}
          </div>
        </div>
        <div
          className="final-cta"
          style={{
            backgroundImage: `linear-gradient(0deg, var(--cta-shade), var(--cta-shade)), url(${sunsetImage})`,
          }}
        >
          <div className="final-cta-content reveal">
            <span className="eyebrow">A whole new perspective</span>
            <h2>
              Ready to see
              <br />
              things differently?
            </h2>
            <p>Start your detection journey today.</p>
            <Button className="button-orange" onClick={() => scrollTo("workspace")}>
              Start detecting <ArrowRight />
            </Button>
            <span className="free-note">↗ It’s free!</span>
          </div>
        </div>
      </section>

      <footer className="site-footer section-light">
        <a className="brand" href="#home">
          <span className="brand-mark">
            <ScanLine size={20} />
          </span>
          <span>
            YOLO <b>Studio</b>
          </span>
        </a>
        <span className="footer-tagline">See the world differently.</span>
        <nav aria-label="Footer navigation">
          <button onClick={() => scrollTo("features")}>Features</button>
          <button onClick={() => scrollTo("about")}>About</button>
          <button onClick={() => scrollTo("how-it-works")}>How it works</button>
        </nav>
        <div className="social-links">
          <a href="https://github.com" target="_blank" rel="noreferrer" aria-label="GitHub">
            <span className="social-github" aria-hidden="true">GH</span>
          </a>
          <a href="https://instagram.com" target="_blank" rel="noreferrer" aria-label="Instagram">
            <span className="social-instagram" aria-hidden="true">IG</span>
          </a>
          <a href="#home" aria-label="Back to top">
            <ArrowUpRight size={17} />
          </a>
        </div>
        <span className="copyright">© 2025 YOLO Studio</span>
      </footer>
      <button className="back-to-top" aria-label="Back to top" onClick={() => scrollTo("home")}>
        <ArrowRight size={16} />
      </button>
    </main>
  );
}
export default HomePage;
