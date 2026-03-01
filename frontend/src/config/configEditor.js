import React, {useState, useEffect} from 'react'
import ItemInput from './itemInput'
import './config.css'

export default function ConfigEditor() {
    const[config, setConfig] = useState(null)

	useEffect(() => {
		fetch("/api/config").then(
			res => res.json()
		).then(
			data => {
				setConfig(data)
            }
		)
	}, [])

    return <div>
        <div className="item-input-container">
            {config && Object.entries(config.items).map(([key, arr]) => (
                <ItemInput itemKey={key} item={arr} setConfig={setConfig}/>
            ))}
        </div>
    </div>
}