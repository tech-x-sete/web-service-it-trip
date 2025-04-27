import React from "react";
import "../EventCard.css"

function EventCard({ event }) {
  return (
    <div className="event">
      <img src={event.image} alt={event.title} className="event-img"/>
      <div className="event-info"> 
        <h3>{event.title}</h3>
        <div className="event-details">
          <span>{event.date}</span> • <span>{event.location}</span>
        </div>
        <div className="event-organization">{event.organization}</div>
        <div className="event-tags"> 
          {event.tags.map(tag => (
           <span className="tag"> {tag} </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default EventCard;
