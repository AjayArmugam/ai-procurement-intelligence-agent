import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Chat from "./pages/Chat";


function App() {

  return (

    <div
      className="
        min-h-screen
        bg-slate-950
        text-white
        px-3 py-4 
        md:p-8
      "
    >

      <div
        className="
          max-w-7xl
          mx-auto
        "
      >

        <h1
          className="
            text-3xl
            md:text-5xl
            font-bold
            mb-6
            md:mb-10
            text-center
          "
        >
          AI Procurement Assistant
        </h1>

        <Dashboard />
        <Analytics />
        <Chat />
        
      </div>

    </div>

  );

}

export default App;