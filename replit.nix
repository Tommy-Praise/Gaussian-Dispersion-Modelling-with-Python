{ pkgs }: {
  deps = [
    pkgs.tk
    pkgs.tcl
    pkgs.qhull
    pkgs.pkg-config
    pkgs.gtk3
    pkgs.gobject-introspection
    pkgs.ghostscript
    pkgs.freetype
    pkgs.ffmpeg-full
    pkgs.cairo
    pkgs.run
    pkgs.glibcLocales
    pkgs.python39Full
    pkgs.python39Packages.pip
    pkgs.python39Packages.streamlit
    pkgs.python39Packages.plotly
];
}