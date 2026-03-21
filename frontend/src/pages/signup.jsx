import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signupUser } from "../api/auth";
import "../styles/Signup.css";

function Signup() {

  const [username,setUsername] = useState("");
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const navigate = useNavigate();

  const handleSignup = async (e)=>{
    e.preventDefault();

    try{
      const res = await signupUser({
        username,
        email,
        password
      });

      console.log(res.data);
      alert("Signup successful");

      // 👉 redirect to login after signup
      navigate("/login");

    }catch(err){
      console.log(err.response?.data);
      alert("Signup failed");
    }
  }

  return(
    <div className="signup-container">
      <div className="signup-card">

        <h2>Create Account</h2>

        <form className="signup-form" onSubmit={handleSignup}>

          <input
            placeholder="Username"
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
            required
          />

          <button type="submit">Sign Up</button>

        </form>

        <p className="signup-switch">
          Already have an account?{" "}
          <span onClick={()=>navigate("/login")}>
            Login
          </span>
        </p>

      </div>
    </div>
  )
}

export default Signup;