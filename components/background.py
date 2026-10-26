"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Subtle Interactive Connected Nodes / Academic Background Component.

Renders an unobtrusive HTML5 canvas particle network in the background.
Uses pointer-events: none so it never interferes with form inputs, buttons, or scrolling.
"""

import streamlit as st

def render_interactive_background() -> None:
    """Inject subtle interactive connected-nodes canvas into the page background."""
    bg_html = """
    <div id="canvas-bg-container" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 0; overflow: hidden; opacity: 0.38;">
        <canvas id="nodeNetworkCanvas"></canvas>
    </div>
    <script>
    (function() {
        const existing = document.getElementById("nodeNetworkCanvas");
        if (!existing) return;
        const canvas = existing;
        const ctx = canvas.getContext("2d");
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener("resize", function() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        const numNodes = 40;
        const nodes = [];
        const colors = ["#2563eb", "#3b82f6", "#1d4ed8", "#60a5fa", "#0ea5e9"];

        for (let i = 0; i < numNodes; i++) {
            nodes.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.45,
                vy: (Math.random() - 0.5) * 0.45,
                radius: Math.random() * 2.2 + 1.2,
                color: colors[Math.floor(Math.random() * colors.length)]
            });
        }

        function step() {
            ctx.clearRect(0, 0, width, height);
            
            // Draw connecting lines between nearby nodes
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dx = nodes[i].x - nodes[j].x;
                    const dy = nodes[i].y - nodes[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 125) {
                        ctx.beginPath();
                        ctx.moveTo(nodes[i].x, nodes[i].y);
                        ctx.lineTo(nodes[j].x, nodes[j].y);
                        ctx.strokeStyle = `rgba(37, 99, 235, ${0.18 * (1 - dist / 125)})`;
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                }
            }

            // Draw and update nodes
            for (let i = 0; i < nodes.length; i++) {
                const n = nodes[i];
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
                ctx.fillStyle = n.color;
                ctx.fill();

                n.x += n.vx;
                n.y += n.vy;

                if (n.x < 0 || n.x > width) n.vx *= -1;
                if (n.y < 0 || n.y > height) n.vy *= -1;
            }

            requestAnimationFrame(step);
        }
        step();
    })();
    </script>
    <style>
    /* Styling refinements for Sri Eshwar branding */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    div[data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    div[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    .sece-header-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        color: #ffffff !important;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .sece-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 800;
        color: #1e3a8a;
        letter-spacing: -0.02em;
        margin-top: 0;
        margin-bottom: 4px;
    }
    .sece-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .sece-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .badge-online {
        background-color: #dbeafe;
        color: #1d4ed8;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 4px;
    }
    .badge-oncampus {
        background-color: #dcfce7;
        color: #15803d;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 4px;
    }
    .badge-async {
        background-color: #fef3c7;
        color: #b45309;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 4px;
    }
    .badge-free {
        background-color: #ecfdf5;
        color: #047857;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.78rem;
    }
    .badge-paid {
        background-color: #f3e8ff;
        color: #6b21a8;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.78rem;
    }
    </style>
    """
    st.components.v1.html(bg_html, height=0)
