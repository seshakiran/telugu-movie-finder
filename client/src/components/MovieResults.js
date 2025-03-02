import React from 'react';

const MovieResults = ({ movies, searchDate }) => {
  if (!movies || !movies.movies || movies.movies.length === 0) {
    return (
      <div className="results">
        <div className="results-header">
          <h2>No Movies Found</h2>
        </div>
        <div className="results-body no-results">
          <p>No Telugu movies were found for the selected date or month.</p>
          <p>Try selecting a different date.</p>
        </div>
      </div>
    );
  }

  const { formatted_date, found_exact_date, movies: movieList } = movies;

  return (
    <div className="results">
      <div className="results-header">
        <h2>
          {found_exact_date
            ? `Telugu Movies Released on ${formatted_date}`
            : `No movies found for ${formatted_date}. Showing movies released in ${formatted_date.split(' ')[0]}`}
        </h2>
      </div>
      <div className="results-body">
        <table className="movie-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Release Date</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            {movieList.map((movie, index) => (
              <tr key={index}>
                <td className="movie-title">
                  {movie.url ? (
                    <a href={movie.url} target="_blank" rel="noopener noreferrer">
                      {movie.title}
                    </a>
                  ) : (
                    movie.title
                  )}
                </td>
                <td className="movie-date">{movie.release_date}</td>
                <td className="movie-summary">{movie.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MovieResults;
