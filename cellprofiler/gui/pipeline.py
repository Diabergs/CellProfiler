import wx

import cellprofiler_core.pipeline

FMT_NATIVE = "Native"


class Pipeline(cellprofiler_core.pipeline.Pipeline):
    def create_progress_dialog(self, message, pipeline, title):
        return wx.ProgressDialog(
            title, message, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_CAN_ABORT
        )

    def respond_to_version_mismatch_error(self, message):
        if wx.GetApp():
            dialog = wx.MessageDialog(
                parent=None,
                message=message + " Continue?",
                caption="Pipeline version mismatch",
                style=wx.OK | wx.CANCEL | wx.ICON_QUESTION,
            )

            if dialog.ShowModal() != wx.ID_OK:
                dialog.Destroy()

                raise cellprofiler_core.pipeline.event.PipelineLoadCancelledException(
                    message
                )

            dialog.Destroy()
        else:
            super(Pipeline, self).respond_to_version_mismatch_error(message)

    def save(self, fd_or_filename, save_image_plane_details=True):
        with open(fd_or_filename, "wt") as fd:
            super(Pipeline, self).dump(fd, save_image_plane_details)
