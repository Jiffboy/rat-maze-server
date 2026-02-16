import React, { useEffect, useState, useRef } from "react";
import DirectionPad from '../components/DirectionPad'
import Item from '../components/Item'
import DebugBar from '../components/DebugBar'
import Timer from '../components/Timer'
import ScrollingText from '../components/ScrollingText'
import './Panels.css'

export default function OnlinePanel({data, socket}) {
  return (
    <div>
      {data.game.is_debug && <DebugBar socket={socket}/>}
      <div className="point-bar">
        <div className="stat-item">
          <span className="stat-label">Current Points:</span>
          <span className="stat-value">{data.user.current_points}</span>
        </div>
        <Timer data={data}/>
        <ScrollingText data={data} text='🧀 Cheese get! 🧀' show={data.user.got_cheese} timestamp={data.game.next_turn}/>
        <div className="stat-item">
          <span className="stat-label">Points All-Time:</span>
          <span className="stat-value">{data.user.total_points}</span>
        </div>
      </div>
      <DirectionPad
        data={data}
        socket={socket}
      />
      <div className="balance-container">
        <span className="stat-label">Balance:</span>
        <span className="stat-value">{data.user.balance}</span>
      </div>

      {data.game.shop.map((item, index) => (
        <Item key={item.name} data={item} balance={data.user.balance} socket={socket}/>
      ))}
    </div>
  );
}
