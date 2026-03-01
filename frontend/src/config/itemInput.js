import React from 'react'
import './config.css'
import TextInput from './textInput'

export default function ItemInput({ itemKey, item, setConfig }) {
  const onChange = (e) => {
    const { name, value } = e.target;

    setConfig((prev) => ({
      ...prev,
      items: {
        ...prev.items,
        [itemKey]: {
          ...prev.items[itemKey],
          [name]: value,
        },
      },
    }));
  };

    return <div className="item-input">
        <h2>{item.name}</h2>
        <p>{item.description}</p>
        <hr/>
        <form className="item-fields">
            <TextInput name="Name" id="name" value={item.name} onChange={onChange}/>
            <TextInput name="Cost" id="cost" value={item.cost} onChange={onChange}/>
            <TextInput name="Stock" id="stock" value={item.stock} onChange={onChange}/>
            <TextInput name="Family" id="family" value={item.family} onChange={onChange}/>
            <TextInput name="Rarity" id="rarity" value={item.rarity} onChange={onChange}/>
            <TextInput name="In Random" id="in_random" value={item.in_random} onChange={onChange}/>
        </form>
    </div>
}