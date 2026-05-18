import { tool, Tool, ToolsProviderController } from "@lmstudio/sdk";
import { z } from "zod";
import * as fs from "fs";
import * as path from "path";

const OBSIDIAN_ROOT = "C:\\ANTIGRAVITY\\1\\obsidian_brain";

// Рекурсивный поиск файлов .md
function searchFiles(dir: string, query: string, results: string[] = []) {
    if (!fs.existsSync(dir)) return results;
    
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            searchFiles(filePath, query, results);
        } else if (filePath.endsWith(".md")) {
            try {
                const content = fs.readFileSync(filePath, "utf-8");
                if (content.toLowerCase().includes(query.toLowerCase()) || file.toLowerCase().includes(query.toLowerCase())) {
                    results.push(`--- FILE: ${filePath.replace(OBSIDIAN_ROOT, '')} ---\n${content.substring(0, 1500)}...\n`);
                }
            } catch (e) {
                // Игнорируем ошибки чтения
            }
        }
    }
    return results;
}

export async function toolsProvider(ctl: ToolsProviderController) {
  const tools: Tool[] = [];

  const readMasterDossierTool = tool({
    name: "read_master_dossier",
    description: "Чтение конкретного Мастер-Досье (ZEUS, BOBOV или MASTODONT) из базы знаний.",
    parameters: {
      dossierName: z.string().describe("Имя досье (ZEUS, BOBOV, MASTODONT)"),
    },
    implementation: async ({ dossierName }) => {
      try {
        let filePath = "";
        const name = String(dossierName).toUpperCase();
        if (name.includes("ZEUS")) {
          filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "ZEUS_MASTER_DOSSIER.md");
        } else if (name.includes("BOBOV")) {
          filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "BOBOV_LEGAL_ATTACK.md");
        } else if (name.includes("MASTODONT")) {
           filePath = path.join(OBSIDIAN_ROOT, "2_KNOWLEDGE", "SYNTHESIS", "MASTODONT_INFRASTRUCTURE.md");
        } else {
          return `Неизвестное досье: ${dossierName}. Доступно: ZEUS, BOBOV, MASTODONT.`;
        }
        
        if (fs.existsSync(filePath)) {
          return fs.readFileSync(filePath, "utf-8");
        }
        return `Файл не найден: ${filePath}`;
      } catch (e) {
        return `Ошибка: ${e}`;
      }
    },
  });
  tools.push(readMasterDossierTool);

  const searchObsidianTool = tool({
    name: "search_obsidian",
    description: "Глобальный поиск по всем Markdown-файлам в базе знаний AntiGravity.",
    parameters: {
      query: z.string().describe("Ключевое слово для поиска (например 'клапан', 'ЕСКД', 'Кража')"),
    },
    implementation: async ({ query }) => {
      try {
        const q = String(query);
        const results = searchFiles(OBSIDIAN_ROOT, q);
        if (results.length === 0) return `Ничего не найдено по запросу: ${q}`;
        return results.slice(0, 3).join("\n\n");
      } catch (e) {
        return `Ошибка поиска: ${e}`;
      }
    },
  });
  tools.push(searchObsidianTool);

  return tools;
}
