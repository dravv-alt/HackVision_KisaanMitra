import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import enUS from 'date-fns/locale/en-US';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import './calendar.css';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon } from 'lucide-react';

const locales = {
    'en-US': enUS,
};

const localizer = dateFnsLocalizer({
    format,
    parse,
    startOfWeek,
    getDay,
    locales,
});

const EventComponent = ({ event }) => {
    let bgColor = '#4CAF50'; // Default Green
    if (event.type === 'check') bgColor = '#FF9800'; // Orange
    if (event.type === 'market') bgColor = '#795548'; // Brown
    if (event.type === 'water') bgColor = '#2196F3'; // Blue

    return (
        <div style={{ backgroundColor: bgColor, padding: '2px 5px', borderRadius: '4px', fontSize: '0.8rem', color: 'white' }}>
            {event.title}
        </div>
    );
};

const CustomToolbar = (toolbar) => {
    const goToBack = () => {
        toolbar.onNavigate('PREV');
    };
    const goToNext = () => {
        toolbar.onNavigate('NEXT');
    };
    const goToCurrent = () => {
        toolbar.onNavigate('TODAY');
    };

    const label = () => {
        const date = toolbar.date;
        return (
            <span style={{ fontWeight: 'bold', fontSize: '1.2rem', color: 'var(--color-text-dark)' }}>
                {format(date, 'MMMM yyyy')}
            </span>
        );
    };

    return (
        <div className="rbc-toolbar" style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="rbc-btn-group">
                    <button type="button" onClick={goToBack} style={{ border: 'none', background: 'transparent', cursor: 'pointer', padding: '4px' }}>
                        <ChevronLeft size={20} />
                    </button>
                    <button type="button" onClick={goToNext} style={{ border: 'none', background: 'transparent', cursor: 'pointer', padding: '4px' }}>
                        <ChevronRight size={20} />
                    </button>
                </span>
                <span className="rbc-toolbar-label" style={{ margin: 0, padding: 0 }}>{label()}</span>
            </div>

            <span className="rbc-btn-group">
                <button type="button" onClick={goToCurrent} style={{ padding: '6px 12px', borderRadius: '8px', border: '1px solid var(--color-border)', backgroundColor: 'white', fontSize: '0.85rem' }}>
                    Today
                </button>
                {/* View toggles can go here if needed */}
            </span>
        </div>
    );
};

const FarmingCalendar = ({ compact = false, style }) => {
    // If compact (Dashboard), show Agenda or Week view with limited height
    // If full (Farm Management), show Month view with full height

    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const res = await fetch('/api/v1/dashboard/timeline');
                const data = await res.json();

                // Convert string dates back to Date objects
                const parsedEvents = data.map(evt => ({
                    ...evt,
                    start: new Date(evt.start),
                    end: new Date(evt.end)
                }));

                setEvents(parsedEvents);
            } catch (error) {
                console.error("Failed to fetch calendar events:", error);
            }
        };

        fetchEvents();
    }, []);

    return (
        <div className={`card ${compact ? 'calendar-compact' : ''}`} style={{ ...style, height: compact ? '400px' : '550px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <div style={{ padding: '8px', backgroundColor: 'rgba(33, 150, 243, 0.1)', borderRadius: '8px', color: '#2196F3' }}>
                    <CalendarIcon size={24} />
                </div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>
                    {compact ? "Today's Tasks" : "Farming Calendar"}
                </h3>
            </div>

            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ flex: 1 }}
                views={compact ? ['agenda', 'day'] : ['month', 'week', 'day', 'agenda']}
                defaultView={compact ? 'agenda' : 'month'}
                components={{
                    event: EventComponent,
                    toolbar: CustomToolbar
                }}
            />
        </div>
    );
};

export default FarmingCalendar;
