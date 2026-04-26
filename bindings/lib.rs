use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod song_parser_lib {
    use pyo3::prelude::*;
    use pyo3::exceptions::PyTypeError;


    #[pyfunction]
    fn song_from_text(text: String, artist: String, title: String) -> PyResult<String> {
        use songbook::file_reader::txt_reader::read_from_txt;

        let (blocks, chord_list) = read_from_txt(&text);
        let metadata = songbook::Metadata{
            artist,
            title,
            key: None,
            capo: None,
            autoscroll_speed: None,
            show_options: None,
        };
        let mut song = songbook::Song {
            blocks,
            chord_list,
            metadata,
            notes: None,
        };
        song.detect_key();
        let song_string = if let Ok(s) = serde_yaml::to_string(&song) { s }
        else { return Err(PyTypeError::new_err("Cannot convert to yaml")) };

        Ok(song_string)
    }

    #[pyfunction]
    fn song_from_text_for_editing(text: String) -> PyResult<String> {
        let mut song = songbook::Song::new("", "");
        song.change_from_edited_str(&text);
        let song_string = if let Ok(s) = serde_yaml::to_string(&song) { s }
        else { return Err(PyTypeError::new_err("Cannot convert to yaml")) };

        Ok(song_string)
    }
}
