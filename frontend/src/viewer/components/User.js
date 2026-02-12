import React, { useState, useEffect } from 'react';
import './User.css';

export default function User({user}) {
  return (
    <div className={'user-container'}>
        <p className={'user-name'}>{user.username}</p>
        <p className={'user-points'}>{user.points}</p>
    </div>
  );
};