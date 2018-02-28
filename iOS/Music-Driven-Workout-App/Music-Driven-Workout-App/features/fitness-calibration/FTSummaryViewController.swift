//
//  FTSummaryViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Christopher Choy on 2/25/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class FTSummaryViewController: UIViewController {

    var viewModel = ViewModel()

    var userid: String!
    var category: String = ""
    var numEx: Int = 3
    var exChoices: [Int] = [Int]()
    var reply: [[String:Any]] = [[String:Any]]()
    
    @IBOutlet weak var tableView: UITableView?
    
    override func viewDidLoad() {
        let request = APIRequest()
        
        super.viewDidLoad()
        print(exChoices, userid, category, numEx)
        let trackedStr = exChoices.map { String($0) }.joined(separator: ",")
        let qstr = "categories=\(category)&numexercises=\(numEx)&exerciseids=\(trackedStr)&key=SoftCon2018"
        request.submitPostLocal(route: "/api/fitness/test/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
            self.reply = request.parseJsonRespone(data: data!)!
            
            let vmitems = self.reply.map { ViewModelItem(item: Model(title: $0["name"] as! String, data: $0)) }
            self.viewModel.setItems(items: vmitems)
            
            
            DispatchQueue.main.async {
                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
                self.tableView?.dataSource = self.viewModel
                self.tableView?.delegate = self.viewModel
                self.tableView?.estimatedRowHeight = 100
                self.tableView?.rowHeight = UITableViewAutomaticDimension
                self.tableView?.allowsMultipleSelection = true
                self.tableView?.separatorStyle = .none
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
