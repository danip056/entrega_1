import { useNavigate } from "react-router-dom";
import LogoutMessage from "./LogoutMessage";
const SingOut = () => {
    const navigate = useNavigate();
    localStorage.removeItem('token');
    navigate("/login");
    return(
        <LogoutMessage/>
      )
      
  }
  
  export default SingOut