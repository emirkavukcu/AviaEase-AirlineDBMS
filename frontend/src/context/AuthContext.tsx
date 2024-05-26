import React, {
  createContext,
  useState,
  useEffect,
  useContext,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { isTokenExpired } from "@/utils/checkTokenExpiry";
import { jwtDecode } from "jwt-decode";

interface AuthContextType {
  user: { token: string } | null;
  login: any;
  logout: () => void;
  loading: boolean;
  userName: string | null;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<{ token: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      if (isTokenExpired(token)) {
        localStorage.removeItem("token");
        setUser(null);
        router.push("/auth/signin");
      } else {
        setUser({ token });
        const decodedToken: any = jwtDecode(token);
        setUserName(decodedToken.name);
      }
    }
    setLoading(false);
  }, [router]);

  const login = async (email: string, password: string) => {
    const response = await fetch("http://127.0.0.1:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      const decodedToken: any = jwtDecode(data.access_token);
      setUser({ token: data.access_token });
      setUserName(decodedToken.name);
      router.push("/");
    } else {
      return "Error";
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    router.push("/auth/signin");
  };

  return (
    <AuthContext.Provider value={{ user, userName, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext) as AuthContextType;
