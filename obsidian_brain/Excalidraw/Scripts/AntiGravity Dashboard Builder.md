/*
 * AntiGravity Hub — Visual Dashboard Builder
 * ============================================
 * Excalidraw Script Engine script.
 * Run via: Excalidraw → kebab menu → "Run Script" → "AntiGravity Dashboard Builder"
 *
 * What it does:
 *   Builds a fully interactive visual hub map with wiki links to all
 *   key notes in the AntiGravity vault. Every colored block is clickable.
 *   Creates a new Excalidraw file: Excalidraw/AntiGravity_Hub.excalidraw.md
 */

const EA = excalidrawAutomate;
EA.reset();

// ============================================================
// HELPERS
// ============================================================

/**
 * Add a styled rectangle with an Obsidian wiki link.
 * Returns the element ID.
 */
const addRect = (x, y, w, h, strokeColor, bgColor, link = null) => {
  EA.style.strokeColor = strokeColor;
  EA.style.backgroundColor = bgColor;
  EA.style.fillStyle = "solid";
  EA.style.strokeWidth = 2;
  EA.style.roughness = 0;
  EA.style.opacity = 100;
  const id = EA.addRect(x, y, w, h);
  if (link) {
    const el = EA.getElement(id);
    el.link = link;
  }
  return id;
};

/**
 * Add a standalone text label (no box, no background).
 */
const addLabel = (x, y, w, h, text, color, fontSize = 14, fontId = 2) => {
  EA.style.strokeColor = color;
  EA.style.backgroundColor = "transparent";
  EA.style.fillStyle = "hachure";
  EA.style.strokeWidth = 1;
  EA.addText(x, y, text, {
    width: w,
    height: h,
    textAlign: "center",
    verticalAlign: "middle",
    fontSize: fontSize,
    fontId: fontId,
    strokeColor: color,
  });
};

/**
 * Convenience: add a clickable colored card (rect + label together).
 */
const addCard = (x, y, w, h, label, strokeColor, bgColor, textColor, link, fontSize = 14) => {
  const id = addRect(x, y, w, h, strokeColor, bgColor, link);
  addLabel(x, y, w, h, label, textColor, fontSize);
  return id;
};

/**
 * Connect two elements with a colored arrow.
 */
const connect = (idA, idB, color = "#868e96") => {
  EA.style.strokeColor = color;
  EA.style.backgroundColor = "transparent";
  EA.style.fillStyle = "hachure";
  EA.style.strokeWidth = 2;
  EA.style.roughness = 1;
  EA.style.opacity = 60;
  EA.connectObjects(idA, null, idB, null, {
    numberOfPoints: 0,
    startArrowHead: "none",
    endArrowHead: "arrow",
    padding: 8,
  });
};

// ============================================================
// TITLE
// ============================================================
EA.style.strokeColor = "transparent";
EA.style.backgroundColor = "transparent";
EA.style.fillStyle = "hachure";
EA.addText(-320, -460, "🛸  AntiGravity — Visual Hub", {
  width: 640,
  height: 55,
  textAlign: "center",
  fontSize: 30,
  fontId: 1,
  strokeColor: "#212529",
});

// ============================================================
// CENTRAL HUB
// ============================================================
const HUB = addCard(
  -90, -55, 180, 90,
  "🛸 HUB\nDASHBOARD.md",
  "#e67e22", "#fff3e0", "#b5551b",
  "[[DASHBOARD.md]]",
  17
);

// ============================================================
// BLOCK 1 — 🎓 LEARNING  (top-left)
// ============================================================
const B1 = addCard(
  -520, -330, 380, 48,
  "🎓 УЧЁБА & КОМПАС-3D",
  "#0b7285", "#e3fafc", "#0b7285",
  "[[1_PROJECTS/KOMPAS_LEARNING/📚 Трекер обучения КОМПАС-3D.md]]",
  16
);
addCard(-520, -268, 380, 36, "📋 KOMPAS_KANBAN", "#1098ad", "#ffffff", "#0b7285",
  "[[1_PROJECTS/KOMPAS_LEARNING/KOMPAS_KANBAN.md]]", 13);
addCard(-520, -220, 380, 36, "📖 Тема 1: Компоновочная сборка (Top-Down)", "#1098ad", "#f8fafb", "#0b7285",
  "[[1_PROJECTS/KOMPAS_LEARNING/Тема 1. Компоновочная сборка.md]]", 12);
addCard(-520, -172, 380, 36, "📖 Тема 2: Сборка червячной передачи", "#1098ad", "#f8fafb", "#0b7285",
  "[[1_PROJECTS/KOMPAS_LEARNING/Тема 2. Сборка червячной передачи.md]]", 12);
addCard(-520, -124, 380, 36, "📋 План работы по клапану DN170", "#1098ad", "#f8fafb", "#0b7285",
  "[[1_PROJECTS/KOMPAS_LEARNING/📋 План работы по клапану DN170.md]]", 12);

// ============================================================
// BLOCK 2 — ⚖️ LEGAL  (top-right)
// ============================================================
const B2 = addCard(
  140, -330, 380, 48,
  "⚖️ ДЕЛО БОБОВА",
  "#c92a2a", "#fff5f5", "#c92a2a",
  "[[1_PROJECTS/BOBOV/complaint_draft_new.md]]",
  16
);
addCard(140, -268, 380, 36, "📋 BOBOV_KANBAN", "#e03131", "#ffffff", "#c92a2a",
  "[[1_PROJECTS/BOBOV/BOBOV_KANBAN.md]]", 13);
addCard(140, -220, 380, 36, "📝 Жалоба в Прокуратуру (финал)", "#e03131", "#f8fafb", "#c92a2a",
  "[[1_PROJECTS/BOBOV/complaint_draft_new.md]]", 12);
addCard(140, -172, 380, 36, "📁 Хронология дела 2025", "#e03131", "#f8fafb", "#c92a2a",
  "[[1_PROJECTS/BOBOV/Case_History/Legal_Attack_2025.md]]", 12);
addCard(140, -124, 380, 36, "✉️ Ультиматум нотариусу", "#e03131", "#f8fafb", "#c92a2a",
  "[[1_PROJECTS/BOBOV/ultimatum_notary_final.md]]", 12);

// ============================================================
// BLOCK 3 — 🐘 MASTODONT  (bottom-left)
// ============================================================
const B3 = addCard(
  -520, 110, 380, 48,
  "🐘 MASTODONT BOT",
  "#2b4590", "#edf2ff", "#2b4590",
  "[[3_META/meta/PROJECT_INDEX.md]]",
  16
);
addCard(-520, 172, 380, 36, "🤖 Claude: Кастомные скиллы", "#3b5bdb", "#f8fafb", "#2b4590",
  "[[4_ARCHIVE/ChatGPT_Projects/Claude_Chat_Custom_Skill.md]]", 12);
addCard(-520, 220, 380, 36, "⚙️ Индекс проекта META", "#3b5bdb", "#f8fafb", "#2b4590",
  "[[3_META/meta/PROJECT_INDEX.md]]", 12);
addCard(-520, 268, 380, 36, "🔌 Obsidian + MCP Guide", "#3b5bdb", "#f8fafb", "#2b4590",
  "[[3_META/obsidian_and_mcp_guide.md]]", 12);

// ============================================================
// BLOCK 4 — 📚 KNOWLEDGE  (bottom-right)
// ============================================================
const B4 = addCard(
  140, 110, 380, 48,
  "📚 БАЗА ЗНАНИЙ & АРХИВ",
  "#2b8a3e", "#ebfbee", "#2b8a3e",
  "[[2_KNOWLEDGE/KNOWLEDGE_INDEX.md]]",
  16
);
addCard(140, 172, 380, 36, "📖 Индекс базы знаний", "#37b24d", "#f8fafb", "#2b8a3e",
  "[[2_KNOWLEDGE/KNOWLEDGE_INDEX.md]]", 12);
addCard(140, 220, 380, 36, "🗄️ Архив и Дампы чатов", "#37b24d", "#f8fafb", "#2b8a3e",
  "[[4_ARCHIVE/ARCHIVE_INDEX.md]]", 12);
addCard(140, 268, 380, 36, "🔧 Лог траблшутинга AutoCAD", "#37b24d", "#f8fafb", "#2b8a3e",
  "[[2_KNOWLEDGE/AutoCAD_Troubleshooting_Log.md]]", 12);

// ============================================================
// ARROWS  hub → blocks
// ============================================================
connect(HUB, B1, "#0b7285");
connect(HUB, B2, "#c92a2a");
connect(HUB, B3, "#2b4590");
connect(HUB, B4, "#2b8a3e");

// ============================================================
// GENERATE FILE
// ============================================================
await EA.create({
  filename: "AntiGravity_Hub",
  foldername: "Excalidraw",
  onNewPane: true,
});
