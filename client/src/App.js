import "./static/css/bootstrap.min.css";
import "./static/css/global.css";

import Options from './pages/options';
import BoardView from "./pages/boardView";
import Error from "./pages/error";

import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>

        <Route path="/board" element={
          <>
            <BoardView/>
          </>
        }/>

        <Route exact path="/" element={
          <>
            <Options/>
          </>
        }/>

        <Route path="*" element={
          <>
            <Error/>
          </>
        }/>

      </Routes>
    </Router>
  );
}

export default App;
