# Copyright (C) 2011-2015 Ilias Stamatis <stamatis.iliass@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import QSettings, QTimer
from PyQt5.QtWidgets import (
        QDialog, QDialogButtonBox, QFileDialog, QLabel, QLineEdit,
        QRadioButton, QSpacerItem, QTabWidget, QToolButton, QWidget,
        QPlainTextEdit, QPushButton
        )

from ffmulticonverter import utils
from ffmulticonverter import config


class Preferences(QDialog):
    def __init__(self, parent=None, test = False):
        super(Preferences, self).__init__(parent)
        self.parent = parent
        self.test = test

        saveQL = QLabel('<html><b>' + self.tr('Save files') + '</b></html>')
        existQL = QLabel(self.tr('Existing files:'))
        self.exst_prefixQRB = QRadioButton(self.tr("Add '~' prefix"))
        self.exst_overwriteQRB = QRadioButton(self.tr('Overwrite'))
        exist_layout = utils.add_to_layout(
                'h', self.exst_prefixQRB, self.exst_overwriteQRB)

        defaultQL = QLabel(self.tr('Default output destination:'))
        self.defaultQLE = QLineEdit()
        self.defaultQTB = QToolButton()
        self.defaultQTB.setText('...')
        deafult_fol_layout = utils.add_to_layout(
                'h', self.defaultQLE, self.defaultQTB)
        nameQL = QLabel('<html><b>' + self.tr('Name files') +'</b></html>')
        prefixQL = QLabel(self.tr('Prefix:'))
        suffixQL = QLabel(self.tr('Suffix:'))
        self.prefixQLE = QLineEdit()
        self.suffixQLE = QLineEdit()
        grid = utils.add_to_grid(
                [prefixQL, self.prefixQLE], [suffixQL, self.suffixQLE])
        prefix_layout = utils.add_to_layout('h', grid, None)

        tabwidget1_layout = utils.add_to_layout(
                'v', saveQL,
                QSpacerItem(14, 13), existQL, exist_layout,
                QSpacerItem(14, 13), defaultQL, deafult_fol_layout,
                QSpacerItem(13, 13), nameQL, QSpacerItem(14, 13),
                prefix_layout, None
                )

        ffmpegQL = QLabel('<html><b>FFmpeg</b></html>')
        default_cmd_ffmpegQL = QLabel(self.tr('Default command:'))
        self.ffmpegcmdQLE = QLineEdit()

        vidcodecsQL = QLabel(
                '<html><b>' + self.tr('Video codecs') +'</b></html>')
        self.vidcodecsQPTE = QPlainTextEdit()
        audcodecsQL = QLabel(
                '<html><b>' + self.tr('Audio codecs') +'</b></html>')
        self.audcodecsQPTE = QPlainTextEdit()
        extraformatsffmpegQL = QLabel(
                '<html><b>' + self.tr('Extra formats') +'</b></html>')
        self.extraformatsffmpegQPTE = QPlainTextEdit()

        gridlayout = utils.add_to_grid(
                [vidcodecsQL, audcodecsQL, extraformatsffmpegQL],
                [self.vidcodecsQPTE, self.audcodecsQPTE,
                 self.extraformatsffmpegQPTE]
                )

        defvidcodecsQPB = QPushButton(self.tr("Default video codecs"))
        defaudcodecsQPB = QPushButton(self.tr("Default audio codecs"))

        hlayout1 = utils.add_to_layout(
                'h', None, defvidcodecsQPB, defaudcodecsQPB)

        tabwidget2_layout = utils.add_to_layout(
                'v', ffmpegQL,
                QSpacerItem(14, 13), default_cmd_ffmpegQL, self.ffmpegcmdQLE,
                QSpacerItem(20, 20), gridlayout, hlayout1, None
                )

        imagemagickQL = QLabel('<html><b>ImageMagick (convert)</b></html>')
        default_cmd_imageQL = QLabel(self.tr('Default options:'))
        self.imagecmdQLE = QLineEdit()

        extraformatsimageQL = QLabel(
                '<html><b>' + self.tr('Extra formats') +'</b></html>')
        self.extraformatsimageQPTE = QPlainTextEdit()

        hlayout2 = utils.add_to_layout('h', self.extraformatsimageQPTE, QSpacerItem(220,20))

        tabwidget3_layout = utils.add_to_layout(
                'v', imagemagickQL,
                QSpacerItem(14,13), default_cmd_imageQL, self.imagecmdQLE,
                QSpacerItem(20,20), extraformatsimageQL, hlayout2, None
                )

        widget1 = QWidget()
        widget1.setLayout(tabwidget1_layout)
        widget2 = QWidget()
        widget2.setLayout(tabwidget2_layout)
        widget3 = QWidget()
        widget3.setLayout(tabwidget3_layout)
        tabWidget = QTabWidget()
        tabWidget.addTab(widget1, self.tr('General'))
        tabWidget.addTab(widget2, self.tr('Audio/Video'))
        tabWidget.addTab(widget3, self.tr('Images'))

        buttonBox = QDialogButtonBox(
                QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

        final_layout = utils.add_to_layout('v', tabWidget, None, buttonBox)
        self.setLayout(final_layout)

        self.defaultQTB.clicked.connect(self.open_dir)
        buttonBox.accepted.connect(self.save_settings)
        buttonBox.rejected.connect(self.reject)
        defvidcodecsQPB.clicked.connect(
                lambda: self.set_videocodecs(config.video_codecs))
        defaudcodecsQPB.clicked.connect(
                lambda: self.set_audiocodecs(config.audio_codecs))

        self.resize(400, 450)
        self.setWindowTitle(self.tr('Preferences'))

        QTimer.singleShot(0, self.load_settings)

    def load_settings(self):
        """Load settings and update graphical widgets with loaded values."""
        settings = QSettings()
        overwrite_existing = settings.value('overwrite_existing', type=bool)
        default_output = settings.value('default_output', type=str)
        prefix = settings.value('prefix', type=str)
        suffix = settings.value('suffix', type=str)
        default_command = settings.value('default_command', type=str)
        videocodecs = (settings.value('videocodecs') or [])
        audiocodecs = (settings.value('audiocodecs') or [])
        extraformats_video = (settings.value('extraformats') or [])
        default_command_image = settings.value('default_command_image', type=str)
        extraformats_image = (settings.value('extraformats_image') or [])

        if overwrite_existing:
            self.exst_overwriteQRB.setChecked(True)
        else:
            self.exst_prefixQRB.setChecked(True)
        if default_output:
            self.defaultQLE.setText(default_output)
        if prefix:
            self.prefixQLE.setText(prefix)
        if suffix:
            self.suffixQLE.setText(suffix)
        if default_command:
            self.ffmpegcmdQLE.setText(default_command)
        else:
            self.ffmpegcmdQLE.setText(config.default_ffmpeg_cmd)

        if not videocodecs:
            videocodecs = config.video_codecs
        if not audiocodecs:
            audiocodecs = config.audio_codecs
        self.set_videocodecs(videocodecs)
        self.set_audiocodecs(audiocodecs)

        self.extraformatsffmpegQPTE.setPlainText("\n".join(extraformats_video))

        if default_command_image:
            self.imagecmdQLE.setText(default_command_image)
        else:
            self.imagecmdQLE.setText(config.default_imagemagick_cmd)

        self.extraformatsimageQPTE.setPlainText("\n".join(extraformats_image))

    def set_videocodecs(self, codecs):
        self.vidcodecsQPTE.setPlainText("\n".join(codecs))

    def set_audiocodecs(self, codecs):
        self.audcodecsQPTE.setPlainText("\n".join(codecs))

    def open_dir(self):
        """Get a directory name using a standard Qt dialog and update
        self.defaultQLE with dir's name."""
        if self.defaultQLE.isEnabled():
            _dir = QFileDialog.getExistingDirectory(
                    self, 'FF Multi Converter - ' +
                    self.tr('Choose default output destination'), config.home
                    )
            if _dir:
                self.defaultQLE.setText(_dir)

    def save_settings(self):
        """Set settings values, extracting the appropriate information from
        the graphical widgets."""
        # remove empty codecs
        videocodecs = []
        audiocodecs = []
        extraformats_video = []
        extraformats_image = []

        for i in self.vidcodecsQPTE.toPlainText().split("\n"):
            i = i.strip()
            if len(i.split()) == 1 and i not in videocodecs: # i single word
                videocodecs.append(i)

        for i in self.audcodecsQPTE.toPlainText().split("\n"):
            i = i.strip()
            if len(i.split()) == 1 and i not in audiocodecs:
                audiocodecs.append(i)

        for i in self.extraformatsffmpegQPTE.toPlainText().split("\n"):
            i = i.strip()
            if len(i.split()) == 1 and i not in extraformats_video \
            and i not in config.video_formats:
                extraformats_video.append(i)

        for i in self.extraformatsimageQPTE.toPlainText().split("\n"):
            i = i.strip()
            if len(i.split()) == 1 and i not in extraformats_image \
            and i not in config.image_formats:
                extraformats_image.append(i)

        settings = QSettings()
        settings.setValue(
                'overwrite_existing', self.exst_overwriteQRB.isChecked())
        settings.setValue(
                'default_output', self.defaultQLE.text())
        settings.setValue(
                'prefix', self.prefixQLE.text())
        settings.setValue(
                'suffix', self.suffixQLE.text())
        settings.setValue(
                'default_command', self.ffmpegcmdQLE.text())
        settings.setValue(
                'videocodecs', sorted(videocodecs))
        settings.setValue(
                'audiocodecs', sorted(audiocodecs))
        settings.setValue(
                'extraformats', sorted(extraformats_video))
        settings.setValue(
                'default_command_image', self.imagecmdQLE.text())
        settings.setValue(
                'extraformats_image', sorted(extraformats_image))

        self.accept()
