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

    #[pyfunction]
    fn can_save() -> bool {
        #[cfg(target_os = "android")]
        return false;

        #[cfg(not(target_os = "android"))]
        return true;
    }

    #[pyfunction]
    fn save(yaml: String) -> PyResult<()> {
        use songbook::song_library::get_lib_path;
        use std::fs;
        use std::io::Write;

        if !can_save() {
            return Err(PyTypeError::new_err("Cannot save songs on android!"));
        }

        let lib_path = if let Ok(p) = get_lib_path() {p}
            else { return Err(PyTypeError::new_err("Cannot get base lib path!"))};

        let song_parser_dir = lib_path.join("song-parser");
        if !song_parser_dir.exists() {
            fs::create_dir_all(&song_parser_dir)?;
        }

        let title = if let Some(t) = get_title_from_yaml(&yaml) {t}
            else { "title".to_string() };

        let artist = if let Some(a) = get_artist_from_yaml(&yaml) {a}
            else { "artist".to_string() };

        let song_name = format!("{title} - {artist}");
        let song_path = get_free_path(song_parser_dir.join(&song_name), &song_name);

        let mut file = fs::File::create(song_path)?;
        file.write_all(yaml.as_bytes())?;


        Ok(())
    }
    fn get_title_from_yaml(yaml: &str) -> Option<String> {
        let keyword = "title: ";
        let start_index = yaml.find(keyword)? + keyword.len();
        let end_index = yaml[start_index..].find("\n")? + start_index;
        
        Some(yaml[start_index..end_index].to_string())
    }
    fn get_artist_from_yaml(yaml: &str) -> Option<String> {
        let keyword = "artist: ";
        let start_index = yaml.find(keyword)? + keyword.len();
        let end_index = yaml[start_index..].find("\n")? + start_index;
        
        Some(yaml[start_index..end_index].to_string())
    }
    fn get_free_path(mut path: std::path::PathBuf, name: &str) -> std::path::PathBuf {
        let mut counter = 1;
        while path.exists() {
            path.set_file_name(&format!("{}({})", name, counter));
            counter += 1;
        }
    
        return path
    }
}
