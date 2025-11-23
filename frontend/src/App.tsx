import AvatarPane from "./components/AvatarPane";
import ChatMessages from "./components/ChatMessages";
import ChatHistory from "./components/ChatHistory";

export default function App() {

  return (
    <div className="flex max-h-screen bg-gradient-to-br from-indigo-200 to-blue-200">
      <AvatarPane />

      {/* Sidebar  */}
      <div className="flex-1 flex flex-col bg-white">
        <ChatMessages />
        <ChatHistory />
      </div>
    </div >
  );
}
