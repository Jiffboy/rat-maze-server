import React, { useState, useEffect } from 'react';
import './User.css';

export default function User({user, rank}) {
  const getRankClass = () => {
    if (rank === 1) return 'rank-1';
    if (rank === 2) return 'rank-2';
    if (rank === 3) return 'rank-3';
    return '';
  };

  return (
    <div className={`user-container ${getRankClass()}`}>
        <span className={'user-rank'}>{rank}</span>
        <p className={'user-name'}>{user.username}</p>
        <p className={'user-points'}>{user.points}</p>
    </div>
  );
};