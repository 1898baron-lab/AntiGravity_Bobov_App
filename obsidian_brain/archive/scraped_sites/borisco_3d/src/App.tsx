import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const App: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // --- THREE.JS SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Procedural Core (TorusKnot)
    const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
    const material = new THREE.MeshPhysicalMaterial({
      color: 0x00f2ff,
      metalness: 0.9,
      roughness: 0.1,
      transmission: 0.5,
      thickness: 1,
      transparent: true,
      emissive: 0x7000ff,
      emissiveIntensity: 0.2
    });
    const core = new THREE.Mesh(geometry, material);
    scene.add(core);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f2ff, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    camera.position.z = 5;

    // --- GSAP ANIMATION ---
    gsap.to(core.rotation, {
      y: Math.PI * 2,
      duration: 10,
      repeat: -1,
      ease: "none"
    });

    // Scroll Animation
    gsap.to(core.scale, {
      x: 2, y: 2, z: 2,
      scrollTrigger: {
        trigger: ".section-2",
        start: "top bottom",
        end: "top top",
        scrub: 1
      }
    });

    gsap.to(core.position, {
      x: -2,
      scrollTrigger: {
        trigger: ".section-3",
        start: "top bottom",
        end: "top top",
        scrub: 1
      }
    });

    // --- RESIZE HANDLER ---
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // --- RENDER LOOP ---
    const animate = () => {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="app-container">
      <canvas ref={canvasRef} id="canvas-container" style={{ position: 'fixed', top: 0, left: 0 }} />
      
      <section className="content-section section-1">
        <div className="glass-panel">
          <h1>Borisco AI</h1>
          <p className="subtitle">FACTORY OF INTELLIGENCE</p>
          <p>Будущее промышленного ИИ начинается здесь. Мы создаем автономные решения для самых сложных задач.</p>
        </div>
      </section>

      <section className="content-section section-2">
        <div className="glass-panel">
          <h2>Scalable Core</h2>
          <p>Наше ядро адаптируется под любые мощности. От локальных серверов до облачных кластеров.</p>
          <div className="feature-grid">
            <div className="feature-card">High Speed</div>
            <div className="feature-card">Infinite Context</div>
            <div className="feature-card">Secure Box</div>
          </div>
        </div>
      </section>

      <section className="content-section section-3">
        <div className="glass-panel" style={{ marginLeft: '40%' }}>
          <h2>Continuous Learning</h2>
          <p>Borisco AI помнит каждый байт информации, становясь умнее с каждым вашим сообщением.</p>
          <button style={{ marginTop: '1rem', padding: '1rem 2rem', background: 'linear-gradient(45deg, #00f2ff, #7000ff)', border: 'none', borderRadius: '12px', color: 'white', fontWeight: 'bold', cursor: 'pointer' }}>
            START CONVERSATION
          </button>
        </div>
      </section>
    </div>
  );
};

export default App;
