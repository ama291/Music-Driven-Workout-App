//
//  ExerciseViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Alex A on 2/13/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit
import CoreMotion

class AccelerometerViewController: UIViewController {

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
    var frequency = ""

    
    @IBOutlet weak var statusLabel: UILabel!
    @IBOutlet weak var frequencyLabel: UILabel!
    
    func getMotionData() {
        self.statusLabel.text = "collecting data..."
        // saving acceleration every 0.1 seconds
        timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(AccelerometerViewController.displayResult), userInfo: nil, repeats: false)
        
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

    //json request struct
    struct jsonRequest: Codable {
        var Result: Float
        var Status: String
    }

    @objc func displayResult() {
        motionManager.stopAccelerometerUpdates()
        self.statusLabel.text = "complete"
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        let decoder = JSONDecoder()
        do {
            let data = try? JSONSerialization.data(withJSONObject: self.motionData, options: .prettyPrinted)
            let json = String(data: data!, encoding: .utf8)
            if let json = json { // converting to a string
                let url = URL(string: "http://138.197.49.155:8000/api/fitness/accel/")!
                var request = URLRequest(url: url)
                request.httpMethod = "POST"
                let postString = "data=" + json + "&key=SoftCon2018"
                request.httpBody = postString.data(using: String.Encoding.utf8)
                let config = URLSessionConfiguration.default
                let session = URLSession(configuration: config)
                let task = session.dataTask(with: request) { (responseData, response, responseError) in
                    guard responseError == nil else {
                        return
                    }
                    if let data = responseData {
                        do {
                            let jsonResponse = try decoder.decode(jsonRequest.self, from: data)
                            self.frequency = String(describing: jsonResponse.Result)
                            print(self.frequency)
                            self.updateLabel()
                        }
                        catch {
                            return
                        }
                    } else {
                        return
                    }
                }
                task.resume()
            }
        }
    }
    
    @objc func updateLabel() {
        //need to fix this to callback
        self.frequencyLabel.text = self.frequency
    }
    
}
