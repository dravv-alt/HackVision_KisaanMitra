import React, { useState } from 'react';
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

// Mock Data
const myEventsList = [
    {
        title: 'Wheat Irrigation',
        start: new Date(new Date().setHours(10, 0, 0)),
        end: new Date(new Date().setHours(12, 0, 0)),
        type: 'water'
    },
    {
        title: 'Apply Fertilizer (DAP)',
        start: new Date(new Date().setDate(new Date().getDate() + 2)),
        end: new Date(new Date().setDate(new Date().getDate() + 2)),
        allDay: true,
        type: 'fertilizer'
    },
    {
        title: 'Pest Check (Aphids)',
        start: new Date(new Date().setDate(new Date().getDate() + 5)),
        end: new Date(new Date().setDate(new Date().getDate() + 5)),
        allDay: true,
        type: 'check'
    },
    {
        title: 'Mandi Visit',
        start: new Date(new Date().setDate(new Date().getDate() + 7)),
        end: new Date(new Date().setDate(new Date().getDate() + 7)),
        allDay: true,
        type: 'market'
    }
];

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
                events={myEventsList}
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
