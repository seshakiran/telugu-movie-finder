import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import MovieResults from './components/MovieResults';
import { searchMoviesByDate } from './utils/api';

function App() {
  const [selectedDate, setSelectedDate] = useState(null);
  const [movies, setMovies] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchPerformed, setSearchPerformed] = useState(false);

  const handleDateChange = (date) => {
    setSelectedDate(date);
    // Reset results when date changes
    if (searchPerformed) {
      setMovies(null);
      setError(null);
      setSearchPerformed(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedDate) {
      setError('Please select a date');
      return;
    }
    
    setLoading(true);
    setError(null);
    setSearchPerformed(true);
    
    try {
      const result = await searchMoviesByDate(selectedDate);
      setMovies(result);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching movie data');
      setMovies(null);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date) => {
    if (!date) return '';
    
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${month}/${day}/${year}`;
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Telugu Movie Finder</h1>
        <p>Search for Telugu movies released on a specific date or month</p>
      </header>
      
      <section className="search-form">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="date-picker">Select a Date (MM/DD/YYYY)</label>
            <DatePicker
              id="date-picker"
              selected={selectedDate}
              onChange={handleDateChange}
              dateFormat="MM/dd/yyyy"
              placeholderText="Select a date"
              className="date-picker"
              maxDate={new Date()}
            />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button 
            type="submit" 
            className="btn" 
            disabled={!selectedDate || loading}
          >
            {loading ? 'Searching...' : 'Search Movies'}
          </button>
        </form>
      </section>
      
      {loading ? (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Searching for movies... This may take a moment.</p>
        </div>
      ) : (
        searchPerformed && movies && (
          <MovieResults 
            movies={movies} 
            searchDate={selectedDate ? formatDate(selectedDate) : ''}
          />
        )
      )}
    </div>
  );
}

export default App;
