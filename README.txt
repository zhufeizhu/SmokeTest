#此工程为ttwebview sdk112版本以上的冒烟测试创建
#目的在于对62和75的so进行冒烟测试
#工程的目录结构如下

smoketest:
|____README.txt
|____debug
|    |____app-debug.apk　
|____androidTest
|    |____app-debug-androidTest.apk
|____sh
     |____run_sdk_smoke_test


#app-debug.apk就是ttwebview_test的debug包
#app-debug-androidTest.apk就是冒烟测试的测试包
#run_sdk_smoke_test就是机架上的测试脚本


{
  "thubRunClass": "run_sdk_smoke_test.SmokeTestRunner",
  "codesDownloadUrl": "http://tosv.byted.org/obj/tostest/run_sdk_smoke_test.py",
  "branchName": "master",
   "Debug_Apk_DownloadUrl":"http://tosv.byted.org/obj/tostest/app-debug.apk",
  "AndroidTest_Apk_DownloadUrl":"http://tosv.byted.org/obj/tostest/app-debug-androidTest.apk",
  "test_so_amount":2
}

