import React, { useState } from 'react';
import ChatPage from './ChatPage';
import SettingsPage from './SettingsPage';

const tabs = [
  { name: 'Chat', component: ChatPage },
  { name: 'Settings', component: SettingsPage }
];

export default function HomePage() {
  const [activeTab, setActiveTab] = useState(0);

  const ActiveComponent = tabs[activeTab].component;

  return (
    <div className="flex flex-col">
      <div className="flex border-b">
        {tabs.map((tab, index) => (
          <button
            key={index}
            onClick={() => setActiveTab(index)}
            className={`px-4 py-2 ${activeTab === index ? 'border-b-2 border-violet-500 text-violet-500' : 'text-gray-500'}`}
          >
            {tab.name}
          </button>
        ))}
      </div>
      <div className="flex-1 overflow-hidden">
        <ActiveComponent />
      </div>
    </div>
  );
}