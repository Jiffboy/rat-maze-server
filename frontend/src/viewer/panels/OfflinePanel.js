import React, { useEffect, useState, useRef } from "react";
import DirectionPad from '../components/DirectionPad'
import Item from '../components/Item'
import User from '../components/User'
import './Panels.css';

export default function OnlinePanel({data, socket}) {
    return (
      <div className="offline-container">
        <p className="offline-status">OFFLINE</p>
        <div className="user-stats">
          <div className="stats-grid">
            <div className="stat-row">
              <span>Last Session:</span>
              <strong>{data.user.current_points}</strong>
            </div>
            <div className="stat-row">
              <span>Total Points:</span>
              <strong>{data.user.total_points}</strong>
            </div>
            <div className="stat-row">
              <span>Total Cheese:</span>
              <strong>{data.user.total_cheese}</strong>
            </div>
          </div>
        </div>

        <div className="leaderboard-section">
          <p className="leaderboard-title">🏆 Leaderboard</p>
          <div className="leaderboard-container">
            {data.leaderboard.map((user, index) => (
              <User key={user.username} user={user} rank={index + 1}/>
            ))}
          </div>
        </div>
      </div>
    )
}