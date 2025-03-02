import axios from 'axios';

/**
 * Formats a Date object to MM/DD/YYYY string format
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
const formatDateForApi = (date) => {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const year = date.getFullYear();
  
  return `${month}/${day}/${year}`;
};

/**
 * Searches for Telugu movies released on a specific date
 * @param {Date} date - The date to search for
 * @returns {Promise<Object>} Movie data response
 * @throws {Error} If the API request fails
 */
export const searchMoviesByDate = async (date) => {
  if (!(date instanceof Date)) {
    throw new Error('Invalid date provided');
  }
  
  const formattedDate = formatDateForApi(date);
  
  try {
    const response = await axios.get(`/api/movies?date=${formattedDate}`);
    
    if (response.status !== 200) {
      throw new Error('Failed to fetch movie data');
    }
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      const errorMessage = error.response.data.error || 'Error fetching movie data';
      throw new Error(errorMessage);
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response from server. Please check your internet connection.');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error('Error setting up request: ' + error.message);
    }
  }
};
