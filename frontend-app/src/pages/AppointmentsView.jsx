import React, { useState, useEffect } from 'react';
import { 
  Calendar as CalendarIcon, 
  MessageSquare, 
  Users, 
  Clock, 
  CheckCircle2, 
  Send, 
  Loader2, 
  UserCheck, 
  MapPin,
  Bot
} from 'lucide-react';
import { api } from '../api';

export default function AppointmentsView() {
  const [activeSubTab, setActiveSubTab] = useState('chat');
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      text: "Hello! I am AegisMed's Appointment Assistant. You can check doctor schedules, search available clinic slots, or book appointments. How can I assist you today?"
    }
  ]);
  const [input, setInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);

  const [doctors, setDoctors] = useState([]);
  const [slots, setSlots] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [slotLoading, setSlotLoading] = useState(false);

  // Slot filter states
  const [specialty, setSpecialty] = useState('All');
  const [period, setPeriod] = useState('all');

  useEffect(() => {
    fetchDoctors();
    fetchBookings();
    fetchSlots();
  }, []);

  const fetchDoctors = async () => {
    const res = await api.getDoctors();
    if (res.data?.doctors) setDoctors(res.data.doctors);
  };

  const fetchBookings = async () => {
    const res = await api.getBookings();
    if (res.data?.bookings) setBookings(res.data.bookings);
  };

  const fetchSlots = async () => {
    setSlotLoading(true);
    const params = { period };
    if (specialty !== 'All') params.specialty = specialty;
    const res = await api.getSlots(params);
    setSlotLoading(false);
    if (res.data) setSlots(res.data);
  };

  const handleSendMessage = async (e) => {
    e?.preventDefault();
    if (!input.trim() || chatLoading) return;

    const userText = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userText }]);
    setChatLoading(true);

    const res = await api.chatAppointment(userText);
    setChatLoading(false);

    if (res.error) {
      setMessages(prev => [...prev, { role: 'bot', text: `Sorry, an error occurred: ${res.error}` }]);
    } else {
      setMessages(prev => [...prev, { role: 'bot', text: res.data?.message || 'Action executed successfully.' }]);
      // Refresh active bookings in case one was created
      fetchBookings();
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-[#0B1340] via-[#12236E] to-[#1E2FE0] text-white p-8 shadow-md">
        <div className="text-xs font-bold uppercase tracking-wider text-blue-200">Booking & Schedules</div>
        <h1 className="text-3xl font-extrabold tracking-tight mt-1 text-white">Appointments Assistant</h1>
        <p className="text-sm text-slate-200 mt-1 max-w-2xl">
          Multi-turn conversational doctor scheduling assistant integrated with active MongoDB booking persistence.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto">
        <button
          onClick={() => setActiveSubTab('chat')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all cursor-pointer whitespace-nowrap ${
            activeSubTab === 'chat' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          💬 Conversational Booking
        </button>
        <button
          onClick={() => setActiveSubTab('doctors')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all cursor-pointer whitespace-nowrap ${
            activeSubTab === 'doctors' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          👨‍⚕️ Doctors Roster ({doctors.length})
        </button>
        <button
          onClick={() => setActiveSubTab('slots')}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all cursor-pointer whitespace-nowrap ${
            activeSubTab === 'slots' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          ⏰ Real-Time Slots
        </button>
        <button
          onClick={() => { setActiveSubTab('bookings'); fetchBookings(); }}
          className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all cursor-pointer whitespace-nowrap ${
            activeSubTab === 'bookings' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          📋 Active Bookings ({bookings.length})
        </button>
      </div>

      {/* Tab 1: Chat Assistant */}
      {activeSubTab === 'chat' && (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[520px]">
          {/* Message List */}
          <div className="flex-1 p-6 overflow-y-auto space-y-4 custom-scrollbar bg-slate-50/40">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {m.role === 'bot' && (
                  <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-xs">
                    <Bot className="w-4 h-4" />
                  </div>
                )}
                <div className={`p-4 rounded-2xl text-sm max-w-lg leading-relaxed shadow-xs ${
                  m.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white text-slate-800 border border-slate-200/90 rounded-bl-none'
                }`}>
                  {m.text}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex gap-3 justify-start items-center">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="bg-white p-3 rounded-2xl border border-slate-200 text-xs text-slate-500 flex items-center gap-2">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Checking doctor roster and slots...</span>
                </div>
              </div>
            )}
          </div>

          {/* Chat Input */}
          <form onSubmit={handleSendMessage} className="p-4 bg-white border-t border-slate-200 flex items-center gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g. 'Book with Dr. Sarah Jenkins tomorrow afternoon at 2pm for Arjun Mehta'..."
              className="flex-1 px-4 py-3 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
            <button
              type="submit"
              disabled={chatLoading || !input.trim()}
              className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-md shadow-blue-500/20 flex items-center gap-2 cursor-pointer disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              <span>Send</span>
            </button>
          </form>
        </div>
      )}

      {/* Tab 2: Doctors Roster */}
      {activeSubTab === 'doctors' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {doctors.map((doc, idx) => (
            <div key={idx} className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm hover:shadow-md transition-shadow space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-blue-50 text-blue-600 font-extrabold flex items-center justify-center text-sm border border-blue-100">
                  {doc.name.split(' ').map(n => n[0]).slice(0, 2).join('')}
                </div>
                <div>
                  <h4 className="font-extrabold text-slate-900 text-base">{doc.name}</h4>
                  <div className="text-xs font-bold text-blue-600">{doc.specialty}</div>
                </div>
              </div>
              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500 font-medium">
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  Clinic: {doc.room}
                </span>
                <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold">Available</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab 3: Real-Time Slots */}
      {activeSubTab === 'slots' && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-sm space-y-6">
          <div className="flex flex-wrap items-center gap-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Specialty</label>
              <select
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
                className="px-3 py-2 rounded-xl border border-slate-200 text-xs font-bold bg-white"
              >
                <option value="All">All Specialties</option>
                <option value="Cardiology">Cardiology</option>
                <option value="Neurology">Neurology</option>
                <option value="Orthopedics">Orthopedics</option>
                <option value="General Medicine">General Medicine</option>
                <option value="Pediatrics">Pediatrics</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Period</label>
              <select
                value={period}
                onChange={(e) => setPeriod(e.target.value)}
                className="px-3 py-2 rounded-xl border border-slate-200 text-xs font-bold bg-white"
              >
                <option value="all">All Day</option>
                <option value="morning">Morning</option>
                <option value="afternoon">Afternoon</option>
                <option value="evening">Evening</option>
              </select>
            </div>

            <div className="self-end">
              <button
                onClick={fetchSlots}
                disabled={slotLoading}
                className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs shadow-xs hover:bg-blue-700 cursor-pointer"
              >
                {slotLoading ? 'Loading...' : 'Filter Slots'}
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 uppercase font-bold">
                <tr>
                  <th className="p-3">Doctor</th>
                  <th className="p-3">Specialty</th>
                  <th className="p-3">Date</th>
                  <th className="p-3">Time</th>
                  <th className="p-3">Room</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {slots.map((s, i) => (
                  <tr key={i} className="hover:bg-slate-50/60 transition-colors">
                    <td className="p-3 font-bold text-slate-900">{s.doctor_name}</td>
                    <td className="p-3 text-blue-600 font-semibold">{s.specialty}</td>
                    <td className="p-3 text-slate-600">{s.date}</td>
                    <td className="p-3 font-mono font-bold text-slate-800">{s.time}</td>
                    <td className="p-3 text-slate-500">{s.room}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200">
                        {s.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 4: Active Bookings */}
      {activeSubTab === 'bookings' && (
        <div className="space-y-4">
          {bookings.length === 0 ? (
            <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 text-slate-500 text-sm">
              No appointments booked yet. Use the Conversational Booking assistant to schedule one!
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {bookings.map((bk, i) => (
                <div key={i} className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-sm flex items-center justify-between">
                  <div className="space-y-1">
                    <div className="text-base font-extrabold text-slate-900">{bk.patient_name}</div>
                    <div className="text-xs font-bold text-blue-600">{bk.doctor_name} · {bk.specialty}</div>
                    <div className="text-xs text-slate-500 flex items-center gap-1 pt-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{bk.date} at {bk.time}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-bold text-xs border border-emerald-200">
                      {bk.status || 'Confirmed'}
                    </span>
                    <div className="text-[10px] text-slate-400 font-mono mt-1">{bk.booking_id}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
