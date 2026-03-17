import Dashboard from "@/components/Dashboard";

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-background text-foreground">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold tracking-tight mb-2">REInt AI Forecast Monitor</h1>
          <p className="text-gray-400">Comparing actual vs. forecasted wind generation (BMRS API).</p>
        </header>
        <Dashboard />
      </div>
    </main>
  );
}
