import React, { useEffect, useState, useRef } from "react";
import DirectionPad from '../components/DirectionPad'
import Item from '../components/Item'
import User from '../components/User'
import './Panels.css';

export default function OnlinePanel({data, socket}) {
    return (
      <div className="offline-container">
        <p>Game is currently offline!</p>
        <p>Come back later!</p>
        <hr/>
        <p>{data.user.username}</p>
        <p><strong>Points Last Session:</strong> {data.user.current_points}</p>
        <p><strong>Total Points All-Time:</strong> {data.user.total_points}</p>
        <p><strong>Total Cheeses All-Time:</strong> {data.user.total_cheese}</p>
        <hr/>
        <p><strong>Leaderboard:</strong></p>
        <div className="leaderboard-container">
          {data.leaderboard.map((user, index) => (
            <User user={user}/>
          ))}
        </div>
      </div>
    )
}