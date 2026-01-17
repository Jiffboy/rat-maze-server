import React, { useEffect, useState, useRef } from "react";
import './App.css'
import ViewerPanel from './viewer/panels/ViewerPanel'
import { Route, Routes } from "react-router-dom"

function App() {
	return (
		<div>
            <Routes>
                <Route path="/" element={<ViewerPanel/>}/>
            </Routes>
		</div>
	)
}

export default App