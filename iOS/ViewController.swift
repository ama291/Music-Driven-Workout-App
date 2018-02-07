//
//  ViewController.swift
//  Accl
//
//  Created by Lucy Newman on 2/4/18.
//  Copyright © 2018 Lucy Newman. All rights reserved.
//

import UIKit
import CoreMotion

class ViewController: UIViewController {
    
    var motionManager = CMMotionManager()
    var motionData: [[String : Double]] = []
    
    var timer = Timer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func viewDidAppear(_ animated: Bool) {
        // saving acceleration every 0.1 seconds
        timer = Timer.scheduledTimer(timeInterval: 30, target: self, selector: #selector(ViewController.printResult), userInfo: nil, repeats: false)
        
        motionManager.accelerometerUpdateInterval = 0.1
        
        motionManager.startAccelerometerUpdates(to: OperationQueue.current!) {(data, error) in
            if let myData = data
            {
                var myDict: [String: Double] = [:]
                myDict = ["xAccl": myData.acceleration.x, "yAccl": myData.acceleration.y, "zAccl": myData.acceleration.z, "timestamp": myData.timestamp]
                
                self.motionData.append(myDict) 
            }
        }
    }
    
    @objc func printResult() {
        // printing the results in JSON format
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        
        do {
            let data = try? JSONSerialization.data(withJSONObject: self.motionData, options: .prettyPrinted )
            let json = String(data: data!, encoding: .utf8)
            if let json = json { // converting to a string
                print(json)
            }
        }
        exit(0)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }   
}
