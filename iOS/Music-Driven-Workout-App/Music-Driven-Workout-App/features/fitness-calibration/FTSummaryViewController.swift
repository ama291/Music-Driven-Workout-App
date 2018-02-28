//
//  FTSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTSummaryViewController: UIViewController {
    
    var userid: String!
    var category: String = ""
    var numEx: Int = 3
    var tracked: [Int] = [12, 144]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        print(category, numEx)
        let requests = APIRequest()
        
        var trackedStr = ""
        for t in tracked {
            trackedStr += String(t) + ","
        }
        let last = trackedStr.count - 1
        trackedStr = trackedStr[0..last]
        
        let qstr = "category=" + category + "&numexercises=" + String(numEx) + "&tracked=" + "&key=SoftCon2018"
        
        request.submitPostLocal(route: "/api/fitness/getexsbytype/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseJsonRespone(data: data!)!
            
            //            names = reply.map { $0["name"] }
            print(self.reply[0]["name"]!)
            for rep in self.reply {
                self.exList.append(rep["name"]! as! String)
            }
            DispatchQueue.main.async {
                self.exPicker.delegate = self
                self.exPicker.dataSource = self
            }
            
            }.resume()
        
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

}
