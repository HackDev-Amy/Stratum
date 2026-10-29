import { useAuth } from "./auth";
import LoginPage from "./components/LoginPage";
import Dashboard from "./components/Dashboard";
import ToastHost from "./components/ui/Toast";

export default function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-2 border-accent border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <>
      {user ? <Dashboard /> : <LoginPage />}
      <ToastHost />
    </>
  );
}