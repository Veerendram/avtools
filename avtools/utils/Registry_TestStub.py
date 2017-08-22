from registry import RegistryHandler

reg = RegistryHandler()
print reg.get_sub_keys(hkey="HKCU",
                       key_path="SOFTWARE\SplitCam\SplitCam")

print reg.get_sub_key_values(hkey="HKCU",
                             key_path="SOFTWARE\SplitCam\SplitCam",
                             sub_key="PlayListOptions")

print reg.get_value_data(hkey="HKCU",
                   key_path="SOFTWARE\SplitCam\SplitCam",
                   sub_key="CurrentParameters", value_name='VideoSource')

print reg.get_value_data(hkey="HKCU",
                   key_path="SOFTWARE\SplitCam\SplitCam",
                   sub_key="PlayListOptions", value_name='LastVideo')

reg.set_value_data(hkey="HKCU",
                   key_path="SOFTWARE\SplitCam\SplitCam",
                   sub_key="CurrentParameters", value_name="VideoSource",
                   value_data="video", value_type="REG_SZ")

print reg.get_value_data(hkey="HKCU",
                   key_path="SOFTWARE\SplitCam\SplitCam",
                   sub_key="CurrentParameters", value_name='VideoSource')

print reg.get_value_data(hkey="HKCU",
                   key_path="SOFTWARE\SplitCam\SplitCam",
                   sub_key="PlayListOptions", value_name='LastVideo')