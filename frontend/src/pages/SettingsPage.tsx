import { useEffect, useState } from "react";

type Settings = {
    persona?: string;
    text_model?: string;
    vision_model?: string;
    voice_model?: string;
    chat_memory?: boolean;
    camera_rotation?: number;
    extra_preset_prompt?: string;
    web_access: boolean;
    ollama_config?: any;
    // Legacy fields (kept for compatibility)
    mode?: "neuro" | "evil_neuro";
    chaos?: number;
};

const API = "http://localhost:5000/api/settings";

export default function SettingsPage() {
    const [settings, setSettings] = useState<Settings | null>(null);

    useEffect(() => {
        fetch(API)
            .then(res => res.json())
            .then(setSettings);
    }, []);

    if (!settings) return <div>Loading...</div>;

    const update = (updated: Settings) => {
        setSettings(updated);
        fetch(API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updated),
        });
    };

    return (
        <div className="p-4 space-y-4">
            <h2 className="text-xl font-bold">Companion Settings</h2>

            {/* Personality Mode */}
            <select
                value={settings.mode || settings.persona || ""}
                onChange={e =>
                    update({ ...settings, mode: e.target.value as any, persona: e.target.value })
                }
            >
                <option value="">Select Mode</option>
                <option value="neuro">Neuro</option>
                <option value="evil_neuro">Evil Neuro</option>
            </select>

            {/* Chaos Slider */}
            <div>
                <label>Chaos: {(settings.chaos ?? 0).toFixed(2)}</label>
                <input
                    type="range"
                    min={0}
                    max={1}
                    step={0.05}
                    value={settings.chaos ?? 0}
                    onChange={e =>
                        update({ ...settings, chaos: parseFloat(e.target.value) })
                    }
                />
            </div>

            {/* Web Access */}
            <label>
                <input
                    type="checkbox"
                    checked={settings.web_access}
                    onChange={e =>
                        update({ ...settings, web_access: e.target.checked })
                    }
                />
                Allow Web Access
            </label>
        </div>
    );
}
