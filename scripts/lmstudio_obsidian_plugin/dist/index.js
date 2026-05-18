"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.toolsProvider = toolsProvider;
const sdk_1 = require("@lmstudio/sdk");
const zod_1 = require("zod");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const OBSIDIAN_ROOT = "C:\\ANTIGRAVITY\\1\\obsidian_brain";
// Рекурсивный поиск файлов .md
function searchFiles(dir, query, results = []) {
    if (!fs.existsSync(dir))
        return results;
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            searchFiles(filePath, query, results);
        }
        else if (filePath.endsWith(".md")) {
            try {
                const content = fs.readFileSync(filePath, "utf-8");
                if (content.toLowerCase().includes(query.toLowerCase()) || file.toLowerCase().includes(query.toLowerCase())) {
                    results.push(`--- FILE: ${filePath.replace(OBSIDIAN_ROOT, '')} ---\n${content.substring(0, 1500)}...\n`);
                }
            }
            catch (e) {
                // Игнорируем ошибки чтения
            }
        }
    }
    return results;
}
async function toolsProvider(ctl) {
    const tools = [];
    const readMasterDossierTool = (0, sdk_1.tool)({
        name: "read_master_dossier",
        description: "Чтение конкретного Мастер-Досье (ZEUS, BOBOV или MASTODONT) из базы знаний.",
        parameters: {
            dossierName: zod_1.z.string().describe("Имя досье (ZEUS, BOBOV, MASTODONT)"),
        },
        implementation: async ({ dossierName }) => {
            try {
                let filePath = "";
                const name = String(dossierName).toUpperCase();
                if (name.includes("ZEUS")) {
                    filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "ZEUS_MASTER_DOSSIER.md");
                }
                else if (name.includes("BOBOV")) {
                    filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "BOBOV_LEGAL_ATTACK.md");
                }
                else if (name.includes("MASTODONT")) {
                    filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "MASTODONT_INFRASTRUCTURE.md");
                }
                else {
                    return `Неизвестное досье: ${dossierName}. Доступно: ZEUS, BOBOV, MASTODONT.`;
                }
                if (fs.existsSync(filePath)) {
                    return fs.readFileSync(filePath, "utf-8");
                }
                return `Файл не найден: ${filePath}`;
            }
            catch (e) {
                return `Ошибка: ${e}`;
            }
        },
    });
    tools.push(readMasterDossierTool);
    const searchObsidianTool = (0, sdk_1.tool)({
        name: "search_obsidian",
        description: "Глобальный поиск по всем Markdown-файлам в базе знаний AntiGravity.",
        parameters: {
            query: zod_1.z.string().describe("Ключевое слово для поиска (например 'клапан', 'ЕСКД', 'Кража')"),
        },
        implementation: async ({ query }) => {
            try {
                const q = String(query);
                const results = searchFiles(OBSIDIAN_ROOT, q);
                if (results.length === 0)
                    return `Ничего не найдено по запросу: ${q}`;
                return results.slice(0, 3).join("\n\n");
            }
            catch (e) {
                return `Ошибка поиска: ${e}`;
            }
        },
    });
    tools.push(searchObsidianTool);
    return tools;
}
