//
//  ExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/13/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import CoreMotion

class ExerciseViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */
    
    @IBAction func exerciseBack(_ sender: Any) {
        performSegue(withIdentifier: "exerciseBackSegue", sender: self)
    }
    
    @IBAction func testAccelerometerClick(_ sender: Any) {
        getMotionData()
    }
    
    var motionManager = CMMotionManager()
    var motionData: [[String : Double]] = []
    var timer = Timer()
    
    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var frequencyLabel: UILabel!
    
    func getMotionData() {
        self.statusLabel.text = "collecting data..."
        // saving acceleration every 0.1 seconds
        timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(ExerciseViewController.displayResult), userInfo: nil, repeats: false)
        
        var dispTime = -0.1;
        motionManager.accelerometerUpdateInterval = 0.1
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {(data, error) in
            if let myData = data
            {
                dispTime += 0.1
                self.statusLabel.text = "collecting data..." + String(format:"%.1f", dispTime) + "s"
                var myDict: [String: Double] = [:]
                myDict = ["xAccl": myData.acceleration.x, "yAccl": myData.acceleration.y, "zAccl": myData.acceleration.z, "timestamp": myData.timestamp]
        
                self.motionData.append(myDict)
            }
        }
    }

    @objc func displayResult() {
        self.statusLabel.text = "complete"
        //let encoder = JSONEncoder()
        //encoder.outputFormatting = .prettyPrinted
        
        do {
            let data = try? JSONSerialization.data(withJSONObject: self.motionData, options: .prettyPrinted)
            let json = String(data: data!, encoding: .utf8)
            if let json = json { // converting to a string
                let url = URL(string: "http://138.197.49.155:8000/api/database/")!
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                var headers = request.allHTTPHeaderFields ?? [:]
                headers["Content-Type"] = "application/json"
                request.allHTTPHeaderFields = headers
                let bodyData = "data=" + json + "&key=SoftCon2018"
                request.httpBody = bodyData.data(using: String.Encoding.utf8)
                let config = URLSessionConfiguration.default
                let session = URLSession(configuration: config)
                let task = session.dataTask(with: request) { (responseData, response, responseError) in
                    guard responseError == nil else {
                        return
                    }
                    if let data = responseData, let utf8Representation = String(data: data, encoding: .utf8) {
                        print("response: ", utf8Representation)
                    } else {
                        print("no readable data received in response")
                    }
                }
                task.resume()
            }
        }
    }
}
