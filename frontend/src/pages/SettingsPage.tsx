import { useEffect, useState } from "react";

type Settings = {
    mode: "neuro" | "evil_neuro";
    chaos: number;
    web_access: boolean;
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
                value={settings.mode}
                onChange={e =>
                    update({ ...settings, mode: e.target.value as any })
                }
            >
                <option value="neuro">Neuro</option>
                <option value="evil_neuro">Evil Neuro</option>
            </select>

            {/* Chaos Slider */}
            <div>
                <label>Chaos: {settings.chaos.toFixed(2)}</label>
                <input
                    type="range"
                    min={0}
                    max={1}
                    step={0.05}
                    value={settings.chaos}
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
