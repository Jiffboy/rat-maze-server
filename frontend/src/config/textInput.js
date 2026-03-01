import React from 'react'
import './config.css'

export default function TextInput({name, id, value, onChange }) {
    return <div className="input">
        <label for={id}>{name}</label>
        <input type="text" id={id} name={id} value={value} onChange={onChange}/>
    </div>
}