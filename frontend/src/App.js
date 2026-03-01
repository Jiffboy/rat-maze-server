import { Route, Routes } from "react-router-dom"
import './App.css'
import ConfigEditor from './config/configEditor'
import AboutPage from './about/aboutPage'
import PrivacyPolicy from './privacy/privacyPolicy'
import Header from './common/header'
import TermsOfService from './tos/tos'

function App() {
    return (
        <div className="App">
            <Header/>
            <Routes>
                <Route path="/" element={<AboutPage/>}/>
                <Route path="/edit" element={<ConfigEditor/>}/>
                <Route path="/privacy" element={<PrivacyPolicy/>}/>
                <Route path="/tos" element={<TermsOfService/>}/>
            </Routes>
        </div>
    );
}

export default App;
