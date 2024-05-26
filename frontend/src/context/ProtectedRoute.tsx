import { ReactNode } from "react";
import { useAuth } from "./AuthContext";
import Loader from "@/components/common/Loader";

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <Loader />;
  }

  if (!user) {
    return <Loader />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
